#!/usr/bin/env python3
"""Expand S1 standardized variants into deterministic joining-context probes."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CONTEXTS = {
    "isolate": ("", ""),
    "initial": ("", "\u200d"),
    "medial": ("\u200d", "\u200d"),
    "final": ("\u200d", ""),
}
SELECTORS = {"\u180b", "\u180c", "\u180d", "\u180f"}


def labels(text: str) -> list[str]:
    return [f"U+{ord(character):04X}" for character in text]


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_s1_context_matrix.py REVIEW_QUEUE OUTPUT")
    queue_path, output_path = map(Path, sys.argv[1:])
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    probes = []
    for task in queue["tasks"]:
        if task["category"] != "standardized_variation_sequence":
            continue
        expected_contexts = set(task["expected"]["shaping_contexts"])
        default = "".join(character for character in task["text"] if character not in SELECTORS)
        contexts = CONTEXTS.items() if expected_contexts else [("context_independent", ("", ""))]
        for context, (prefix, suffix) in contexts:
            target_text = f"{prefix}{task['text']}{suffix}"
            default_text = f"{prefix}{default}{suffix}"
            probes.append({
                "id": f"{task['id']}-{context}",
                "task_id": task["id"],
                "context": context,
                "desired_appearance": task["expected"]["desired_appearance"],
                "expectation_class": "normative_target" if not expected_contexts or context in expected_contexts else "outside_declared_context",
                "target_text": target_text,
                "target_code_points": labels(target_text),
                "default_text": default_text,
                "default_code_points": labels(default_text),
                "context_method": "ZWJ-controlled joining context",
                "source": task["source"],
            })
    if len(probes) != 234:
        raise ValueError(f"expected 234 probes, got {len(probes)}")
    payload = {
        "schema_version": "1.0.0",
        "generated_at": queue["generated_at"],
        "method": {
            "description": "Each standardized sequence is compared with its selector-free default in four ZWJ-controlled joining contexts.",
            "assertion": "Visible glyph response changes in the shaping contexts listed by Unicode; other contexts are diagnostic only.",
            "boundary": "A matching response proves contextual selector behavior, not linguistic or calligraphic correctness.",
        },
        "summary": {
            "probe_count": len(probes),
            "task_count": len({probe["task_id"] for probe in probes}),
            "context_count": len(CONTEXTS),
            "normative_target_count": sum(probe["expectation_class"] == "normative_target" for probe in probes),
        },
        "probes": probes,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
