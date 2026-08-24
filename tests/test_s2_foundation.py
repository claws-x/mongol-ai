import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PhaseS2FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "data/engine/s2-semantic-registry.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "data/corpus/sources.json").read_text(encoding="utf-8"))
        cls.observations = json.loads((ROOT / "data/corpus/observations.json").read_text(encoding="utf-8"))
        cls.joining = json.loads((ROOT / "data/unicode/joining-types-17.0.0.json").read_text(encoding="utf-8"))

    def test_joining_data_is_version_locked_to_unicode_17(self):
        self.assertEqual(self.joining["unicodeVersion"], "17.0.0")
        self.assertEqual(self.joining["property"], "Joining_Type")
        self.assertRegex(self.joining["sourceSha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(self.joining["defaultValue"], "U")
        values = {record["value"] for record in self.joining["ranges"]}
        self.assertTrue({"C", "D", "T"}.issubset(values))

    def test_semantic_registry_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "registry.json"
            subprocess.run([
                "node",
                str(ROOT / "scripts/build_s2_semantic_registry.mjs"),
                str(ROOT / "data/quality/s1-review-queue.json"),
                str(ROOT / "data/quality/s1-context-matrix.json"),
                str(ROOT / "data/quality/s1-machine-evidence.json"),
                str(output),
            ], check=True)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), self.registry)

    def test_registry_has_93_unique_semantic_roles_and_honest_backend_states(self):
        targets = self.registry["targets"]
        self.assertEqual(len(targets), 93)
        self.assertEqual(len({target["semanticRole"] for target in targets}), 93)
        self.assertEqual(sum(self.registry["summary"]["byBackendStatus"].values()), 93)
        a_medial_form3 = next(target for target in targets if target["semanticRole"] == "MONGOLIAN_A.medial.form3")
        self.assertEqual(a_medial_form3["inputSequence"], ["U+1820", "U+180C"])
        self.assertEqual(a_medial_form3["backend"]["status"], "project-glyph-required")

    def test_sources_are_explicit_about_license_and_disabled_transport_failures(self):
        self.assertGreaterEqual(len(self.sources["sources"]), 5)
        for source in self.sources["sources"]:
            self.assertTrue(source["seedUrls"])
            self.assertTrue(source["license"])
            self.assertIs(source["redistributable"], False)
            if not source["enabled"]:
                self.assertTrue(source.get("selectionReason"))
        tls_disabled = [source for source in self.sources["sources"] if "TLS" in source.get("disabledReason", "")]
        self.assertEqual(len(tls_disabled), 2)

    def test_committed_observations_are_short_lossless_codepoint_records(self):
        self.assertEqual(self.observations["schemaVersion"], "1.0.0")
        self.assertGreaterEqual(len(self.observations["documents"]), 2)
        self.assertEqual(self.observations["failures"], [])
        for document in self.observations["documents"]:
            self.assertFalse(document["redistributable"])
            self.assertRegex(document["contentHash"], r"^sha256:[0-9a-f]{64}$")
            self.assertEqual(document["segmentCount"], len(document["segments"]))
            for segment in document["segments"]:
                self.assertLessEqual(len(segment["codepoints"]), 256)
                self.assertEqual(len(segment["codepoints"]), len(segment["text"]))


if __name__ == "__main__":
    unittest.main()
