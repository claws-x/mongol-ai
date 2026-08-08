# Repository handoff

Before planning or changing this repository, read
[`docs/00_PROJECT_CHARTER.md`](docs/00_PROJECT_CHARTER.md) completely.

That charter is the highest-priority project fact source. In particular:

- the product is a deterministic Traditional Mongolian semantic-glyph and vertical-layout engine, not a CSS-only demo;
- public Traditional Mongolian web text is acquired as code points plus context through a reproducible corpus crawler;
- screenshots are only for visual regression and are never glyph truth;
- Unicode, fonts, input methods, shaping libraries, websites, and human opinions are evidence sources, not sole authorities;
- original input and format controls must remain lossless, while controls must not be drawn as body glyphs;
- development must not wait for per-glyph human approval;
- never copy proprietary font outlines or guess closed encoding mappings.

Current main phase: **S2 semantic glyph computation engine**. Locate each task in the
pipeline `input → semantics → glyph → geometry → vertical output`, and keep rules,
evidence, implementation observations, and visual regression results separate.
