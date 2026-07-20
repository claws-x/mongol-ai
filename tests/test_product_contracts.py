import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProductContractTests(unittest.TestCase):
    def test_official_experience_uses_native_vertical_layout(self):
        html = (ROOT / "demos/input/ai-chat.html").read_text(encoding="utf-8")
        self.assertIn("writing-mode: vertical-lr", html)
        self.assertNotIn("rotate(90deg)", html)

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
