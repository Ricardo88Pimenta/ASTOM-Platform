#!/usr/bin/env python3
"""Testes controlados do protótipo de interface ASTOM."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "ui" / "astom-ui.py"
STATIC = ROOT / "ui" / "control-center"
FIXTURE = STATIC / "demo-state.json"

spec = importlib.util.spec_from_file_location("astom_ui", SERVER_PATH)
assert spec and spec.loader
astom_ui = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = astom_ui
spec.loader.exec_module(astom_ui)


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.tags: list[str] = []
        self.lang = ""
        self.inline_handlers: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        data = dict(attrs)
        if tag == "html":
            self.lang = data.get("lang") or ""
        if data.get("id"):
            self.ids.add(str(data["id"]))
        self.inline_handlers.extend(key for key, _ in attrs if key.startswith("on"))


class InterfaceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = astom_ui.criar_servidor(
            "127.0.0.1",
            0,
            STATIC,
            astom_ui.provedor_fixture(FIXTURE),
        )
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path: str, method: str = "GET") -> tuple[int, dict[str, str], bytes]:
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}", method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=3) as response:
                return response.status, {key.lower(): value for key, value in response.headers.items()}, response.read()
        except urllib.error.HTTPError as error:
            return error.code, {key.lower(): value for key, value in error.headers.items()}, error.read()

    def test_python_syntax(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(SERVER_PATH)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_design_tokens(self) -> None:
        tokens = json.loads((STATIC / "tokens.json").read_text(encoding="utf-8"))
        self.assertEqual(tokens["schema_version"], 1)
        self.assertEqual(tokens["status"], "experimental")
        self.assertIn("accent", tokens["color"])
        self.assertGreaterEqual(tokens["typography"]["minimum_body_px"], 12)

    def test_fixture_schema(self) -> None:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        astom_ui.validar_estado(data)
        self.assertEqual(data["source"], "demo")
        self.assertGreater(len(data["planner"]["components"]), 5)
        self.assertGreater(len(data["recovery"]["checks"]), 3)

    def test_html_semantics_and_accessibility(self) -> None:
        parser = StructureParser()
        parser.feed((STATIC / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(parser.lang, "pt-BR")
        self.assertIn("main", parser.tags)
        self.assertIn("nav", parser.tags)
        self.assertIn("conteudo", parser.ids)
        self.assertIn("launcher", parser.ids)
        self.assertFalse(parser.inline_handlers)

    def test_no_external_dependencies(self) -> None:
        combined = "\n".join(
            (STATIC / name).read_text(encoding="utf-8")
            for name in ("index.html", "styles.css", "app.js")
        )
        self.assertNotIn("https://", combined)
        self.assertNotIn("http://", combined)
        self.assertNotIn("cdn.", combined.lower())

    def test_css_integrity(self) -> None:
        css = (STATIC / "styles.css").read_text(encoding="utf-8")
        self.assertEqual(css.count("{"), css.count("}"))
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn(":focus-visible", css)

    def test_javascript_syntax_when_node_is_available(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js não disponível")
        result = subprocess.run(
            [node, "--check", str(STATIC / "app.js")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_health_endpoint(self) -> None:
        status, headers, body = self.request("/api/health")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["mode"], "read-only")
        self.assertEqual(headers.get("cache-control"), "no-store")

    def test_state_endpoint(self) -> None:
        status, headers, body = self.request("/api/state")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["source"], "demo")
        self.assertIn("default-src 'self'", headers.get("content-security-policy", ""))
        self.assertEqual(headers.get("x-content-type-options"), "nosniff")

    def test_static_assets(self) -> None:
        for path, content_type in (
            ("/", "text/html"),
            ("/styles.css", "text/css"),
            ("/app.js", "text/javascript"),
        ):
            status, headers, body = self.request(path)
            self.assertEqual(status, 200, path)
            self.assertTrue(body, path)
            self.assertIn(content_type, headers.get("content-type", ""))

    def test_mutating_methods_are_blocked(self) -> None:
        status, _, body = self.request("/api/state", method="POST")
        data = json.loads(body)
        self.assertEqual(status, 405)
        self.assertIn("não aceita operações mutáveis", data["message"])

    def test_path_traversal_is_not_served(self) -> None:
        status, _, _ = self.request("/%2e%2e/%2e%2e/etc/passwd")
        self.assertNotEqual(status, 200)

    def test_live_collection_contract_with_fake_collectors(self) -> None:
        with tempfile.TemporaryDirectory(prefix="astom-ui-test-") as temp:
            root = Path(temp)
            (root / "core").mkdir()
            (root / "profiles").mkdir()
            manifest = root / "profiles" / "test.json"
            manifest.write_text("{}\n", encoding="utf-8")

            planner = root / "core" / "astom-planejar.py"
            planner.write_text(
                """#!/usr/bin/env python3
import argparse, json
p=argparse.ArgumentParser(); p.add_argument('--manifest'); p.add_argument('--output'); p.add_argument('--json-output'); a=p.parse_args()
open(a.output,'w').write('plano')
json.dump({'profile':{'id':'fake','title':'Fake'},'target':[],'components':[],'summary':{}},open(a.json_output,'w'))
""",
                encoding="utf-8",
            )
            preflight = root / "core" / "astom-preflight-recuperacao.py"
            preflight.write_text(
                """#!/usr/bin/env python3
import argparse, json
p=argparse.ArgumentParser(); p.add_argument('--output'); p.add_argument('--json-output'); a=p.parse_args()
open(a.output,'w').write('preflight')
json.dump({'gate':'bloqueado para criação de snapshot','checks':[]},open(a.json_output,'w'))
""",
                encoding="utf-8",
            )

            data = astom_ui.coletar_estado(root, manifest)
            self.assertEqual(data["source"], "live")
            self.assertEqual(data["planner"]["profile"]["id"], "fake")
            self.assertIn("bloqueado", data["recovery"]["gate"])

    def test_invalid_fixture_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.json"
            path.write_text('{"schema_version": 2}', encoding="utf-8")
            provider = astom_ui.provedor_fixture(path)
            with self.assertRaises(astom_ui.ErroInterface):
                provider()


if __name__ == "__main__":
    unittest.main(verbosity=2)
