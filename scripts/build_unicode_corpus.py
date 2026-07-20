#!/usr/bin/env python3
"""Build the Phase 0 Unicode corpus from Unicode 17 normative data.

The generated corpus proves code-point structure and provenance only. It does not
claim that a particular font renders the desired glyph or that a sequence is
linguistically correct in every Mongolian writing tradition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import unicodedata
from pathlib import Path


UNICODE_VERSION = "17.0.0"
SOURCE_URL = "https://www.unicode.org/Public/17.0.0/ucd/StandardizedVariants.txt"
SOURCE_SHA256 = "f55100b2fb11d3d75a37b8c1ab752192dbd1c4b12328c5ec6b38e3807c0ca597"
CHAPTER_URL = "https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-13/"
CHART_URL = "https://www.unicode.org/charts/PDF/U1800.pdf"


def codepoint_label(value: int) -> str:
    return f"U+{value:04X}"


def character_name(value: int) -> str:
    return unicodedata.name(chr(value), "UNASSIGNED")


def review_state(*, encoding: str = "verified_official") -> dict:
    return {
        "encoding": encoding,
        "glyph_rendering": "pending_cross_browser_and_expert_review",
        "linguistic_usage": "pending_native_speaker_review",
    }


def source_ref(url: str, section: str, line: int | None = None) -> dict:
    result = {"url": url, "section": section}
    if line is not None:
        result["source_line"] = line
    return result


def parse_standardized_variants(path: Path) -> list[dict]:
    raw = path.read_bytes()
    actual_hash = hashlib.sha256(raw).hexdigest()
    if actual_hash != SOURCE_SHA256:
        raise ValueError(
            f"Unexpected source SHA-256: {actual_hash}; expected {SOURCE_SHA256}"
        )

    cases = []
    for line_number, raw_line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if "# MONGOLIAN" not in raw_line:
            continue

        data, comment = raw_line.split("#", 1)
        fields = [field.strip() for field in data.split(";")]
        values = [int(item, 16) for item in fields[0].split()]
        contexts = fields[2].split() if len(fields) > 2 and fields[2] else []
        case_number = len(cases) + 1
        cases.append(
            {
                "id": f"stdvar-{case_number:03d}",
                "category": "standardized_variation_sequence",
                "text": "".join(chr(value) for value in values),
                "codepoints": [codepoint_label(value) for value in values],
                "unicode_names": [character_name(value) for value in values],
                "expected": {
                    "encoding_status": "standardized_variation_sequence",
                    "desired_appearance": fields[1],
                    "shaping_contexts": contexts,
                    "base_character": comment.strip(),
                },
                "source": source_ref(
                    SOURCE_URL, "Mongolian standardized variation sequences", line_number
                ),
                "review": review_state(),
            }
        )

    if len(cases) != 60:
        raise ValueError(f"Expected 60 Mongolian standardized variants, found {len(cases)}")
    return cases


def build_base_character_cases() -> list[dict]:
    cases = []
    for index, value in enumerate(range(0x1820, 0x1843), 1):
        cases.append(
            {
                "id": f"base-{index:03d}",
                "category": "base_character",
                "text": chr(value),
                "codepoints": [codepoint_label(value)],
                "unicode_names": [character_name(value)],
                "expected": {
                    "encoding_status": "assigned_mongolian_character",
                    "range": "Mongolian letters U+1820..U+1842",
                },
                "source": source_ref(CHART_URL, "Mongolian Unicode block chart"),
                "review": review_state(),
            }
        )
    return cases


def build_punctuation_cases() -> list[dict]:
    cases = []
    for index, value in enumerate(range(0x1800, 0x180B), 1):
        cases.append(
            {
                "id": f"punct-{index:03d}",
                "category": "punctuation_or_mark",
                "text": chr(value),
                "codepoints": [codepoint_label(value)],
                "unicode_names": [character_name(value)],
                "expected": {
                    "encoding_status": "assigned_mongolian_punctuation_or_mark"
                },
                "source": source_ref(CHART_URL, "Mongolian Unicode block chart"),
                "review": review_state(),
            }
        )
    return cases


def build_format_control_cases() -> list[dict]:
    definitions = [
        (0x180B, "FVS1", "standalone variation selector is ignored"),
        (0x180C, "FVS2", "standalone variation selector is ignored"),
        (0x180D, "FVS3", "standalone variation selector is ignored"),
        (0x180F, "FVS4", "standalone variation selector is ignored"),
        (0x180E, "MVS", "format control requires contextual review"),
        (0x202F, "NNBSP", "suffix separator requires contextual review"),
    ]
    cases = []
    for index, (value, label, behavior) in enumerate(definitions, 1):
        cases.append(
            {
                "id": f"control-{index:03d}",
                "category": "format_control",
                "text": chr(value),
                "codepoints": [codepoint_label(value)],
                "unicode_names": [character_name(value)],
                "expected": {
                    "encoding_status": "assigned_format_control",
                    "short_name": label,
                    "standalone_behavior": behavior,
                },
                "source": source_ref(CHAPTER_URL, "Section 13.5 Mongolian"),
                "review": review_state(),
            }
        )
    return cases


def build_corpus(source_path: Path) -> dict:
    cases = (
        parse_standardized_variants(source_path)
        + build_base_character_cases()
        + build_punctuation_cases()
        + build_format_control_cases()
    )
    return {
        "schema_version": "1.0",
        "unicode_version": UNICODE_VERSION,
        "status": "encoding_baseline_only",
        "generated_from": {
            "url": SOURCE_URL,
            "sha256": SOURCE_SHA256,
            "retrieved_for_project": "2026-07-20",
        },
        "caveats": [
            "Unicode 17 warns that Mongolian standardized variants are not yet fully synchronized with current practice in UTN #57.",
            "Encoding verification does not prove font rendering or linguistic correctness.",
            "Glyph rendering and linguistic usage remain pending expert review.",
        ],
        "case_count": len(cases),
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Unicode StandardizedVariants.txt")
    parser.add_argument("output", type=Path, help="Output JSON path")
    args = parser.parse_args()

    corpus = build_corpus(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {corpus['case_count']} cases to {args.output}")


if __name__ == "__main__":
    main()
