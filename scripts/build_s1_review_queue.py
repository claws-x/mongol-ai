#!/usr/bin/env python3
"""Build the first Phase S1 review queue from the official Unicode baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def priority(category: str) -> str:
    if category in {"standardized_variation_sequence", "format_control"}:
        return "P0"
    if category == "base_character":
        return "P1"
    return "P2"


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_s1_review_queue.py INPUT OUTPUT")
    source_path, output_path = map(Path, sys.argv[1:])
    corpus = json.loads(source_path.read_text(encoding="utf-8"))
    by_category = {
        name: [case for case in corpus["cases"] if case["category"] == name]
        for name in {"standardized_variation_sequence", "base_character", "format_control"}
    }
    selected = (
        by_category["standardized_variation_sequence"][:60]
        + by_category["base_character"][:35]
        + by_category["format_control"][:5]
    )
    if len(selected) != 100:
        raise ValueError(f"expected 100 seed cases, got {len(selected)}")
    tasks = []
    for case in selected:
        tasks.append({
            "id": f"s1-{case['id']}",
            "status": "captured",
            "priority": priority(case["category"]),
            "category": case["category"],
            "text": case["text"],
            "code_points": case["codepoints"],
            "unicode_names": case.get("unicode_names", []),
            "source": case["source"],
            "requirements": [
                "capture_onon_mn_or_mark_not_applicable",
                "capture_reference_screenshot",
                "record_font_and_input_method_versions",
                "machine_compare_glyphs",
                "native_speaker_or_qualified_reviewer_decision"
            ]
        })
    payload = {
        "schema_version": "1.0.0",
        "generated_at": "2026-08-08",
        "source": {
            "name": "Mongol AI Unicode quality corpus",
            "url": "https://www.unicode.org/Public/17.0.0/ucd/StandardizedVariants.txt",
            "unicode_version": corpus["unicode_version"]
        },
        "summary": {
            "task_count": len(tasks),
            "approved_count": 0,
            "linguist_verified_count": 0
        },
        "tasks": tasks
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
