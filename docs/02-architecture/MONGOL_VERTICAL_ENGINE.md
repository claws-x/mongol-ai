# Mongol AI Vertical Engine 2.0

## Product decision

Traditional Mongolian is stored as continuous Unicode text and shaped by an
OpenType-aware browser engine. The product does not rotate the DOM, draw text
on Canvas, convert text to SVG paths, or split words into character nodes.

The canonical layout is:

```css
writing-mode: vertical-lr;
text-orientation: mixed;
```

This makes the inline direction top-to-bottom and advances subsequent columns
from left to right. `upright` must not be applied to a complete Mongolian run:
it prevents the horizontal font run from being rotated as a connected vertical
run and can leave the visible glyphs looking horizontal and disconnected.

## Engine layers

1. **Unicode integrity** — source text, FVS1–FVS4, MVS, NNBSP, ZWJ and ZWNJ are
   preserved. Rendering never normalizes or rewrites user text.
2. **Deterministic font** — Noto Sans Mongolian v3.002 is self-hosted under the
   SIL Open Font License so GitHub Pages does not depend on Google Fonts or a
   platform-specific system font.
3. **Native shaping** — the browser applies OpenType contextual shaping to a
   continuous string. No manual initial/medial/final glyph substitution occurs.
4. **Capability probe** — the engine compares the horizontal shaped-run width
   with its vertical inline extent and verifies that a forced second column
   advances to the right.
5. **Measured fallback** — `mixed` is the primary mode. `sideways` is selected
   only when the native probe fails and the compatibility probe succeeds. No
   user-agent sniffing is used.
6. **Dynamic upgrade** — a MutationObserver upgrades new messages without
   changing their text nodes.

## Runtime contract

Elements opt in with:

```html
<div lang="mn-Mong" data-mongol-vertical>...</div>
```

After startup, the document exposes:

- `data-mongol-engine-status="ready|degraded"`
- `data-mongol-engine-mode="native|compat|unavailable"`
- `window.MongolAI.vertical.getReport()`
- the `mongolai:vertical-ready` event

The engine API also exposes `validateText(text)` to detect replacement
characters and orphan Mongolian variation selectors without modifying input.

## Acceptance gates

- words remain connected and run from top to bottom;
- wrapped columns advance from left to right;
- the official experience contains no `rotate(90deg)` or full-run `upright`;
- the self-hosted font loads before the runtime reports its final mode;
- dynamic messages receive the same rendering contract;
- source Unicode code points survive input, display and deletion.
