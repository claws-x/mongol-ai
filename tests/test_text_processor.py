import unittest

from core.mongolian_text import MongolianTextProcessor


class MongolianTextProcessorTests(unittest.TestCase):
    def setUp(self):
        self.processor = MongolianTextProcessor()

    def test_detects_and_extracts_mongolian_text(self):
        text = "Hello ᠮᠣᠩᠭᠣᠯ World"
        self.assertTrue(self.processor.is_mongolian(text))
        self.assertEqual(self.processor.extract_mongolian(text), "ᠮᠣᠩᠭᠣᠯ")

    def test_normalize_collapses_whitespace_without_losing_controls(self):
        text = "  ᠰᠠᠶᠢᠨ   ᠪᠠᠶᠢᠨ᠎ᠠ  "
        self.assertEqual(self.processor.normalize(text), "ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ")

    def test_character_counts_are_stable(self):
        stats = self.processor.count_characters("ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ")
        self.assertEqual(stats["words"], 2)
        self.assertGreater(stats["mongolian"], 0)


if __name__ == "__main__":
    unittest.main()
