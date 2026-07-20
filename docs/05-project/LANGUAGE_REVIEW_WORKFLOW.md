# Language and glyph review workflow

This workflow separates three questions that must not be collapsed into one score:

1. Is the Unicode sequence structurally valid and traceable to an official source?
2. Does the target font/browser render the intended glyph in the required context?
3. Is the word, phrase, transliteration and gloss linguistically appropriate for the stated standard or region?

## Reviewer roles

- **Encoding reviewer**: familiar with Unicode Mongolian controls, FVS, MVS and NNBSP.
- **Language reviewer**: fluent reader/writer of the relevant Traditional Mongolian standard or regional usage.
- **Product reviewer**: checks that explanations and correction messages are understandable to the intended user.

One person may fill more than one role, but every accepted language entry requires at least two independent reviews, including one language reviewer. Disputed entries remain `needs_resolution`; they are not silently converted into a single “correct” form.

## Allowed decisions

- `accepted`: suitable for the named standard and documented context.
- `accepted_with_scope`: suitable only for a named region, register, font or shaping context.
- `needs_changes`: proposed correction is recorded but not yet accepted.
- `needs_resolution`: reviewers disagree or the source is insufficient.
- `rejected`: unsuitable, with a reason and preserved audit history.

## Required evidence

Every completed review must record:

- case or entry ID;
- reviewer ID and role;
- standard, dialect or regional scope;
- font name and version for glyph review;
- browser/engine and operating system for rendering review;
- source publication or URL where applicable;
- decision, notes and timestamp;
- screenshot path for visible glyph claims.

Do not store personal contact information in the repository. Reviewer IDs may be pseudonymous; public attribution requires explicit consent.

## Review sequence

1. Automated checks validate schema, code points and source fields.
2. Encoding reviewer checks controls and shaping context.
3. Language reviewers independently assess form, transliteration and gloss.
4. Conflicts are recorded and resolved in a separate decision, never by overwriting earlier reviews.
5. Only `accepted` or appropriately scoped `accepted_with_scope` entries may move into production suggestions.

## Current queues

- `data/quality/mongolian-unicode-cases.json`: encoding and glyph-rendering cases.
- `data/quality/lexicon-review-queue.json`: 99 legacy words and 16 legacy phrases awaiting provenance and language review.

The existing product data remains experimental until entries complete this workflow.

`quality_flags` are mechanical review hints, not corrections or rejection decisions. The current generator flags exact duplicate forms and Cyrillic characters inside the legacy transliteration field so reviewers can triage them first.
