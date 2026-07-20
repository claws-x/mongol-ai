import unittest

from nlp import MongolianParser, MongolianPOSTagger, MongolianTokenizer


class NLPBaselineTests(unittest.TestCase):
    def setUp(self):
        self.tokenizer = MongolianTokenizer()

    def test_tokenizer_imports_and_splits_words(self):
        tokens = self.tokenizer.tokenize("ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ")
        self.assertEqual(tokens, ["ᠮᠣᠩᠭᠣᠯ", "ᠬᠡᠯᠡ"])

    def test_pos_tagger_and_parser_construct(self):
        tagger = MongolianPOSTagger()
        parser = MongolianParser()
        tagged = tagger.tag(["ᠮᠣᠩᠭᠣᠯ", "ᠬᠡᠯᠡ"])
        self.assertEqual(len(tagged), 2)
        self.assertIsNotNone(parser.parse(tagged))


if __name__ == "__main__":
    unittest.main()
