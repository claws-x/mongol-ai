import json
import re
import unittest
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "data" / "knowledge"


class KnowledgeBaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (KNOWLEDGE / "knowledge-base.json").read_text(encoding="utf-8")
        )
        cls.schema = json.loads(
            (KNOWLEDGE / "schema.json").read_text(encoding="utf-8")
        )
        cls.source_ids = {source["id"] for source in cls.data["sources"]}
        cls.institution_ids = {
            institution["id"] for institution in cls.data["institutions"]
        }

    def test_top_level_contract_and_minimum_credible_coverage(self):
        required = {
            "schema_version",
            "updated_at",
            "methodology",
            "sources",
            "institutions",
            "people",
            "publications",
            "resources",
            "standards",
            "coverage",
        }
        self.assertEqual(required, set(self.data))
        self.assertEqual(self.data["schema_version"], "1.0.0")
        self.assertGreaterEqual(len(self.data["sources"]), 25)
        self.assertGreaterEqual(len(self.data["institutions"]), 10)
        self.assertGreaterEqual(len(self.data["people"]), 18)
        self.assertGreaterEqual(len(self.data["publications"]), 10)
        self.assertGreaterEqual(len(self.data["resources"]), 8)
        self.assertGreaterEqual(len(self.data["standards"]), 5)

    def test_ids_are_unique_within_every_entity_type(self):
        for key in (
            "sources",
            "institutions",
            "people",
            "publications",
            "resources",
            "standards",
        ):
            ids = [record["id"] for record in self.data[key]]
            self.assertEqual(len(ids), len(set(ids)), f"duplicate ID in {key}")

    def test_every_relationship_resolves(self):
        for key in ("institutions", "people", "publications", "resources", "standards"):
            for record in self.data[key]:
                self.assertTrue(record["source_ids"], record["id"])
                self.assertTrue(
                    set(record["source_ids"]).issubset(self.source_ids),
                    f"broken source reference in {record['id']}",
                )
        for person in self.data["people"]:
            self.assertTrue(
                set(person["affiliation_ids"]).issubset(self.institution_ids),
                f"broken affiliation reference in {person['id']}",
            )

    def test_sources_are_dated_https_primary_or_original_records(self):
        allowed_types = {
            "standard_body",
            "official_institution",
            "peer_reviewed",
            "preprint",
            "official_repository",
        }
        for source in self.data["sources"]:
            parsed = urlparse(source["url"])
            self.assertEqual(parsed.scheme, "https", source["id"])
            self.assertTrue(parsed.netloc, source["id"])
            self.assertIn(source["source_type"], allowed_types)
            self.assertIn(source["tier"], {"A", "B"})
            accessed = date.fromisoformat(source["accessed_at"])
            self.assertLessEqual(accessed, date.today())

    def test_script_scope_is_explicit_and_separates_writing_systems(self):
        allowed = {"traditional", "cyrillic", "mixed", "unspecified"}
        for key in ("institutions", "people", "publications", "resources", "standards"):
            for record in self.data[key]:
                scopes = record["script_scope"]
                self.assertTrue(scopes, record["id"])
                self.assertTrue(set(scopes).issubset(allowed), record["id"])
        self.assertTrue(
            any("unspecified" in item["script_scope"] for item in self.data["publications"]),
            "ambiguous Mongolian research must not be silently labelled Traditional Mongolian",
        )

    def test_publication_status_does_not_upgrade_preprints(self):
        sources = {source["id"]: source for source in self.data["sources"]}
        for publication in self.data["publications"]:
            cited_types = {
                sources[source_id]["source_type"]
                for source_id in publication["source_ids"]
            }
            if publication["publication_status"] == "preprint":
                self.assertIn("preprint", cited_types)
                self.assertEqual(publication["verification"], "provisional")
            if publication["publication_status"] == "peer_reviewed":
                self.assertIn("peer_reviewed", cited_types)

    def test_authoritative_data_has_no_legacy_placeholders_or_hype(self):
        serialized = json.dumps(self.data, ensure_ascii=False)
        forbidden = [
            r"user=xxx",
            r"0000-0000-0000-0000",
            r"example\.com",
            r"全球首个系统化",
            r"100%正确",
            r"完全支持所有浏览器",
        ]
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, serialized, re.IGNORECASE), pattern)

    def test_coverage_report_admits_non_exhaustive_scope(self):
        gaps = " ".join(self.data["coverage"]["known_gaps"])
        self.assertGreaterEqual(len(self.data["coverage"]["known_gaps"]), 5)
        self.assertIn("不声称全球穷尽", gaps)
        date.fromisoformat(self.data["coverage"]["next_review_at"])

    def test_public_browser_uses_safe_dom_rendering(self):
        html = (ROOT / "knowledge" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "knowledge" / "knowledge-base.js").read_text(encoding="utf-8")
        self.assertIn("knowledge-base.js", html)
        self.assertIn("mongolian_layout_engine.js", html)
        self.assertIn("fetch(DATA_URL", script)
        self.assertIn("textContent", script)
        self.assertNotIn("innerHTML", html + script)
        self.assertIn('rel = "noopener noreferrer"', script)

    def test_json_schema_declares_closed_top_level_contract(self):
        self.assertEqual(
            self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
        )
        self.assertFalse(self.schema["additionalProperties"])
        self.assertEqual(self.schema["properties"]["schema_version"]["const"], "1.0.0")


if __name__ == "__main__":
    unittest.main()
