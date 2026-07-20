#!/usr/bin/env python3
"""Convert legacy vocabulary data into an auditable expert-review queue."""

from __future__ import annotations

import argparse
import json
import unicodedata
from collections import Counter
from pathlib import Path


def build_entry(
    kind: str, index: int, item: dict, source: dict, form_counts: Counter
) -> dict:
    form = item["mongolian"]
    transliteration = item.get("pinyin", "")
    quality_flags = []
    if form_counts[form] > 1:
        quality_flags.append("duplicate_form_in_legacy_source")
    if any("CYRILLIC" in unicodedata.name(character, "") for character in transliteration):
        quality_flags.append("transliteration_contains_cyrillic")

    return {
        "id": f"{kind}-{index:03d}",
        "kind": kind,
        "form": form,
        "codepoints": [f"U+{ord(character):04X}" for character in form],
        "current_chinese_gloss": item.get("chinese", ""),
        "current_transliteration": transliteration,
        "quality_flags": quality_flags,
        "provenance": {
            "source_file": "data/vocabulary.json",
            "source_version": source.get("version"),
            "source_created": source.get("created"),
            "origin": "legacy_seed_data",
            "author_or_institution": None,
            "publication": None,
            "url": None,
            "license": None,
        },
        "review": {
            "status": "unreviewed",
            "reviewed_by": [],
            "reviewed_at": None,
            "dialect_or_standard": None,
            "decision": None,
            "notes": [],
        },
    }


def build_queue(source: dict) -> dict:
    entries = []
    all_items = source.get("words", []) + source.get("phrases", [])
    form_counts = Counter(item["mongolian"] for item in all_items)
    for index, item in enumerate(source.get("words", []), 1):
        entries.append(build_entry("word", index, item, source, form_counts))
    for index, item in enumerate(source.get("phrases", []), 1):
        entries.append(build_entry("phrase", index, item, source, form_counts))

    return {
        "schema_version": "1.0",
        "status": "expert_review_required",
        "generated_from": "data/vocabulary.json",
        "entry_count": len(entries),
        "review_policy": "docs/05-project/LANGUAGE_REVIEW_WORKFLOW.md",
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    source = json.loads(args.source.read_text(encoding="utf-8"))
    queue = build_queue(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {queue['entry_count']} review entries to {args.output}")


if __name__ == "__main__":
    main()
