import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / "data" / "quality"


def labels_for(text):
    return [f"U+{ord(character):04X}" for character in text]


class UnicodeCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = json.loads(
            (QUALITY / "mongolian-unicode-cases.json").read_text(encoding="utf-8")
        )
        cls.cases = cls.corpus["cases"]

    def test_has_at_least_one_hundred_traceable_cases(self):
        self.assertGreaterEqual(len(self.cases), 100)
        self.assertEqual(self.corpus["case_count"], len(self.cases))
        self.assertEqual(len({case["id"] for case in self.cases}), len(self.cases))
        self.assertTrue(all(case["source"]["url"].startswith("https://www.unicode.org/") for case in self.cases))

    def test_codepoint_labels_match_text_exactly(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(case["codepoints"], labels_for(case["text"]))

    def test_standardized_variants_have_valid_fvs_position(self):
        variants = [
            case
            for case in self.cases
            if case["category"] == "standardized_variation_sequence"
        ]
        self.assertEqual(len(variants), 60)
        for case in variants:
            with self.subTest(case=case["id"]):
                self.assertEqual(len(case["text"]), 2)
                self.assertIn(ord(case["text"][1]), {0x180B, 0x180C, 0x180D, 0x180F})
                self.assertEqual(case["review"]["encoding"], "verified_official")

    def test_corpus_does_not_claim_completed_glyph_or_language_review(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["review"]["glyph_rendering"].startswith("pending_"))
                self.assertTrue(case["review"]["linguistic_usage"].startswith("pending_"))


class LexiconReviewQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads(
            (QUALITY / "lexicon-review-queue.json").read_text(encoding="utf-8")
        )
        cls.entries = cls.queue["entries"]

    def test_every_legacy_entry_is_queued(self):
        self.assertEqual(len(self.entries), 115)
        self.assertEqual(self.queue["entry_count"], len(self.entries))
        self.assertEqual(len({entry["id"] for entry in self.entries}), len(self.entries))

    def test_entries_start_unreviewed_with_provenance_slots(self):
        required = {
            "source_file",
            "source_version",
            "origin",
            "author_or_institution",
            "publication",
            "url",
            "license",
        }
        for entry in self.entries:
            with self.subTest(entry=entry["id"]):
                self.assertEqual(entry["codepoints"], labels_for(entry["form"]))
                self.assertEqual(entry["review"]["status"], "unreviewed")
                self.assertTrue(required.issubset(set(entry["provenance"])))

    def test_objective_legacy_data_anomalies_are_flagged(self):
        flagged = {
            entry["id"]: set(entry["quality_flags"])
            for entry in self.entries
            if entry["quality_flags"]
        }
        self.assertIn("transliteration_contains_cyrillic", flagged["phrase-010"])
        duplicate_entries = [
            entry
            for entry in self.entries
            if "duplicate_form_in_legacy_source" in entry["quality_flags"]
        ]
        self.assertGreaterEqual(len(duplicate_entries), 4)


if __name__ == "__main__":
    unittest.main()
