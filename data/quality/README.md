# Unicode quality corpus

`mongolian-unicode-cases.json` is the Phase 0 machine-readable encoding baseline.

It contains:

- 60 Mongolian standardized variation sequences from Unicode 17.0.0.
- 35 assigned Mongolian base letters from U+1820 through U+1842.
- 11 assigned punctuation or mark characters from U+1800 through U+180A.
- 6 format-control cases covering FVS1–FVS4, MVS and NNBSP.

The corpus verifies provenance and code-point structure. It does not assert that a font renders the desired glyph or that a sequence is linguistically appropriate.

## Rebuild

Download the normative Unicode source:

```bash
curl -sS https://www.unicode.org/Public/17.0.0/ucd/StandardizedVariants.txt \
  -o /tmp/StandardizedVariants-17.0.0.txt
python3 scripts/build_unicode_corpus.py \
  /tmp/StandardizedVariants-17.0.0.txt \
  data/quality/mongolian-unicode-cases.json
```

The builder checks the expected SHA-256 before generating output.

## Review states

- `verified_official`: code-point sequence is present in an official Unicode source.
- `pending_cross_browser_and_expert_review`: desired glyph must still be checked with target fonts and browser engines.
- `pending_native_speaker_review`: linguistic use must still be checked by qualified reviewers.

`lexicon-review-queue.json` preserves all 99 legacy words and 16 legacy phrases without silently correcting them. Mechanical `quality_flags` currently identify exact duplicate forms and Cyrillic characters found in the legacy transliteration field; reviewers make the final decision.

## Phase S1 correctness evidence

`s1-review-queue.json` is the first operational review queue. It contains exactly 100 seed tasks selected reproducibly from the Unicode baseline:

- 60 standardized variation sequences;
- 35 assigned base characters;
- 5 format controls.

All 100 tasks begin in `captured`. None is represented as linguistically verified or approved. The browser workbench at `review/index.html` stores working records in local IndexedDB and exports portable JSON evidence bundles conforming to `s1-evidence-bundle.schema.json`.

Rebuild the queue without network access:

```bash
python3 scripts/build_s1_review_queue.py \
  data/quality/mongolian-unicode-cases.json \
  data/quality/s1-review-queue.json
```

The state machine prevents `approved` unless the record includes a locked machine rendering, a named qualified reviewer, a correct decision, a reference screenshot, input-method and font versions, an Onon MN capture or explicit exception, and review notes. This gate proves evidence completeness, not that the human judgment itself is correct.
