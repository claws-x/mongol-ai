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
