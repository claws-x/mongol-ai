import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PhaseS1ReviewPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads((ROOT / "data/quality/s1-review-queue.json").read_text(encoding="utf-8"))

    def test_seed_queue_is_exactly_100_unapproved_tasks(self):
        tasks = self.queue["tasks"]
        self.assertEqual(len(tasks), 100)
        self.assertEqual(len({task["id"] for task in tasks}), 100)
        self.assertEqual(Counter(task["category"] for task in tasks), {
            "standardized_variation_sequence": 60,
            "base_character": 35,
            "format_control": 5,
        })
        self.assertTrue(all(task["status"] == "captured" for task in tasks))
        self.assertEqual(self.queue["summary"]["approved_count"], 0)
        self.assertEqual(self.queue["summary"]["linguist_verified_count"], 0)

    def test_every_seed_has_traceable_source_and_evidence_requirements(self):
        required = {
            "capture_onon_mn_or_mark_not_applicable",
            "capture_reference_screenshot",
            "record_font_and_input_method_versions",
            "machine_compare_glyphs",
            "native_speaker_or_qualified_reviewer_decision",
        }
        for task in self.queue["tasks"]:
            self.assertRegex(task["source"]["url"], r"^https://")
            self.assertTrue(task["text"])
            self.assertTrue(task["code_points"])
            self.assertTrue(task["expected"])
            self.assertEqual(set(task["requirements"]), required)

    def test_queue_builder_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "queue.json"
            subprocess.run([
                sys.executable,
                str(ROOT / "scripts/build_s1_review_queue.py"),
                str(ROOT / "data/quality/mongolian-unicode-cases.json"),
                str(output),
            ], check=True)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), self.queue)

    def test_context_matrix_is_reproducible_and_scoped(self):
        committed = json.loads((ROOT / "data/quality/s1-context-matrix.json").read_text(encoding="utf-8"))
        self.assertEqual(committed["summary"]["probe_count"], 234)
        self.assertEqual(committed["summary"]["normative_target_count"], 93)
        self.assertEqual(Counter(probe["expectation_class"] for probe in committed["probes"]), {
            "normative_target": 93,
            "outside_declared_context": 141,
        })
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "matrix.json"
            subprocess.run([
                sys.executable,
                str(ROOT / "scripts/build_s1_context_matrix.py"),
                str(ROOT / "data/quality/s1-review-queue.json"),
                str(output),
            ], check=True)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), committed)

    def test_schemas_are_closed_and_cover_review_states(self):
        queue_schema = json.loads((ROOT / "data/quality/s1-review-queue.schema.json").read_text(encoding="utf-8"))
        evidence_schema = json.loads((ROOT / "data/quality/s1-evidence-bundle.schema.json").read_text(encoding="utf-8"))
        machine_schema = json.loads((ROOT / "data/quality/s1-machine-evidence.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(queue_schema["additionalProperties"])
        self.assertFalse(evidence_schema["additionalProperties"])
        states = {"captured", "machine_verified", "linguist_verified", "approved", "rejected"}
        self.assertEqual(set(queue_schema["$defs"]["task"]["properties"]["status"]["enum"]), states)
        self.assertEqual(set(evidence_schema["properties"]["status"]["enum"]), states)
        self.assertEqual(machine_schema["properties"]["summary"]["properties"]["task_count"]["const"], 100)

    def test_review_workbench_contains_real_evidence_controls(self):
        html = (ROOT / "review/index.html").read_text(encoding="utf-8")
        script = (ROOT / "review/review.mjs").read_text(encoding="utf-8")
        for profile in ["unicode_national", "onon_mn", "onon_mk", "onon_mw", "menksoft_raw"]:
            self.assertIn(f'data-input-profile="{profile}"', html)
        for control in ["reference-image", "reference-font", "glyph-table", "target-status", "export-record", "import-record"]:
            self.assertIn(f'id="{control}"', html)
        self.assertIn('indexedDB.open(DB_NAME, 1)', script)
        self.assertIn('initFromFontBytes', script)
        self.assertIn('EXPERT_ROLES', script)
        self.assertIn('currentRecord.review.decision === "correct"', script)
        self.assertIn('currentRecord.reference.image_data_url', script)
        self.assertIn('allowedFrom[target].has(currentRecord.status)', script)
        self.assertIn('evaluateCorrectnessTask', script)
        self.assertIn('readonly', html)
        self.assertNotRegex(script, r"https?://[^\"']+\.(?:ttf|otf)")


if __name__ == "__main__":
    unittest.main()
