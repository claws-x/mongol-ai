import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProductContractTests(unittest.TestCase):
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

    def test_rendering_lab_keeps_the_failed_upright_control_visible(self):
        lab = (ROOT / "demos/tests/vertical-engine-lab.html").read_text(encoding="utf-8")
        self.assertIn("现有错误方案", lab)
        self.assertIn("vertical-lr + upright", lab)
        self.assertIn("vertical-lr + mixed", lab)

    def test_official_experience_does_not_inject_user_html(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", html)
        self.assertIn("textContent", html)

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
