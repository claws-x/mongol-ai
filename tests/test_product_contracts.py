import re
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProductContractTests(unittest.TestCase):
    def test_pages_engine_uses_locked_publishable_runtime(self):
        core = (ROOT / "core/mongolian_super_engine.mjs").read_text(encoding="utf-8")
        vendor = ROOT / "assets/vendor/harfbuzzjs"
        manifest = json.loads((vendor / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn('../assets/vendor/harfbuzzjs/index.mjs', core)
        self.assertNotRegex(core, r'from\s+["\'][^"\']*node_modules/')
        for name, expected in manifest["files"].items():
            self.assertEqual(hashlib.sha256((vendor / name).read_bytes()).hexdigest(), expected)

    def test_engine_page_reports_module_load_failure_instead_of_hanging(self):
        html = (ROOT / "engine/index.html").read_text(encoding="utf-8")
        bootstrap = (ROOT / "engine/engine-bootstrap.js").read_text(encoding="utf-8")
        self.assertRegex(html, r'<script src="engine-bootstrap\.js\?v=[0-9.]+"></script>')
        self.assertLess(html.index("engine-bootstrap.js"), html.index("engine-lab.mjs"))
        self.assertIn("引擎资源加载失败", bootstrap)
        self.assertIn("mongol-engine-ready", bootstrap)

    def test_engine_page_exposes_s2_context_trace(self):
        html = (ROOT / "engine/index.html").read_text(encoding="utf-8")
        script = (ROOT / "engine/engine-lab.mjs").read_text(encoding="utf-8")
        self.assertIn('id="semantic-body"', html)
        self.assertIn("Unicode Joining_Type 17.0.0", html)
        self.assertIn("SemanticGlyphRegistry", script)
        self.assertIn("semanticTrace", script)
        self.assertIn('id="lexical-control-body"', html)
        self.assertIn("analyzeMongolianLexicalControls", script)
        self.assertIn("Unicode 16.0 起 MVS", html)

    def test_engine_runtime_urls_are_versioned_with_package_release(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        version = package["version"]
        html = (ROOT / "engine/index.html").read_text(encoding="utf-8")
        script = (ROOT / "engine/engine-lab.mjs").read_text(encoding="utf-8")
        self.assertIn(f'engine-lab.mjs?v={version}', html)
        self.assertIn(f'engine-bootstrap.js?v={version}', html)
        self.assertIn(f'mongolian_super_engine.mjs?v={version}', script)
        self.assertIn(f'semantic_glyph_engine.mjs?v={version}', script)
        self.assertIn(f'mongolian_lexical_controls.mjs?v={version}', script)
        self.assertIn(f's2-semantic-registry.json?v={version}', script)

    def test_official_experience_uses_native_vertical_layout(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        engine_css = (ROOT / "core/mongolian_layout_engine.css").read_text(encoding="utf-8")
        self.assertIn("writing-mode: vertical-lr", engine_css)
        self.assertIn("text-orientation: mixed", engine_css)
        self.assertNotIn("text-orientation: upright", html)
        self.assertNotIn("rotate(90deg)", html)

    def test_official_experience_uses_the_vertical_engine(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        self.assertIn("../../core/mongolian_layout_engine.css", html)
        self.assertIn("../../core/mongolian_layout_engine.js", html)
        self.assertIn("data-mongol-vertical", html)
        self.assertIn('lang="mn-Mong"', html)

    def test_vertical_engine_is_capability_based_and_preserves_text(self):
        engine = (ROOT / "core/mongolian_layout_engine.js").read_text(encoding="utf-8")
        self.assertIn('CSS.supports("writing-mode", "vertical-lr")', engine)
        self.assertIn('this.probe("mixed")', engine)
        self.assertIn('this.probe("sideways")', engine)
        self.assertNotIn("navigator.userAgent", engine)
        self.assertNotIn("letterSpacing: options", engine)
        self.assertIn("element.textContent = text", engine)

    def test_vertical_engine_font_is_self_hosted_with_license(self):
        self.assertTrue((ROOT / "assets/fonts/NotoSansMongolian-Regular.ttf").is_file())
        license_text = (ROOT / "assets/fonts/OFL.txt").read_text(encoding="utf-8")
        self.assertIn("SIL OPEN FONT LICENSE Version 1.1", license_text)

    def test_workspace_exposes_phase_one_document_actions(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        script = (ROOT / "demos/input/ai-chat.js").read_text(encoding="utf-8")
        self.assertIn('id="live-preview"', html)
        self.assertIn('id="copy-button"', html)
        self.assertIn('id="download-button"', html)
        self.assertIn("localStorage.setItem", script)
        self.assertIn("text/plain;charset=utf-8", script)

    def test_workspace_exposes_phase_two_encoding_diagnostics(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        inspector = (ROOT / "core/mongolian_text_inspector.js").read_text(encoding="utf-8")
        self.assertIn('id="diagnostic-list"', html)
        self.assertIn("orphan-fvs", inspector)
        self.assertIn("replacement-character", inspector)
        self.assertIn("matchedCases", inspector)
        self.assertNotIn("navigator.userAgent", inspector)

    def test_rendering_lab_keeps_the_failed_upright_control_visible(self):
        lab = (ROOT / "demos/tests/vertical-engine-lab.html").read_text(encoding="utf-8")
        self.assertIn("现有错误方案", lab)
        self.assertIn("vertical-lr + upright", lab)
        self.assertIn("vertical-lr + mixed", lab)

    def test_official_experience_does_not_inject_user_html(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        script = (ROOT / "demos/input/ai-chat.js").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", html + script)
        self.assertIn("textContent", script)

    def test_official_experience_uses_semantic_keyboard_controls(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        self.assertIn('class="key', html)
        self.assertIsNone(re.search(r'<div class="key(?:\s|")', html))
        self.assertIn('aria-live="polite"', html)

    def test_homepage_exposes_one_primary_product_action(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('data-primary-action="true"'), 1)
        self.assertIn("Labs", html)


if __name__ == "__main__":
    unittest.main()
