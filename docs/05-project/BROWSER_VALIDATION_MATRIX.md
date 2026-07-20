# Browser validation matrix

This matrix defines the remaining Phase 0 visual and interaction checks. Blank results are intentionally not treated as passes.

## Target environments

| ID | Engine | Browser | Operating system | Viewport | Status |
|---|---|---|---|---|---|
| BLINK-DESKTOP | Blink | Codex in-app browser | macOS 26.5.2 | 1280 × 720 | vertical engine gates passed 2026-07-20 |
| WEBKIT-DESKTOP | WebKit | Safari 26.5.2 | macOS 26.5.2 | desktop window | vertical engine gates passed 2026-07-20 |
| GECKO-DESKTOP | Gecko | Firefox stable | macOS | 1280 × 720 | blocked: Firefox is not installed |
| WEBKIT-MOBILE | WebKit | iOS Safari | iPhone-class | 390 × 844 | pending |
| BLINK-MOBILE | Blink | Android Chrome | Android phone-class | 390 × 844 | pending |

Record exact browser, engine and OS versions when a run begins.

## Focused Vertical Engine 2.0 validation — 2026-07-20

The Blink and WebKit desktop runs both reported `mode=native` and
`status=ready`. The following blocking engine checks passed in both available
engines:

- the self-hosted Noto Sans Mongolian v3.002 font loaded;
- a continuous Mongolian word rendered as a connected top-to-bottom run;
- a forced second column advanced to the right;
- the official textarea and dynamically inserted messages used the same mode;
- the formal page contained no full-run `upright` or rotation transform.

Blink additionally passed long-message wrapping and deletion of a base letter
plus FVS1 as one grapheme. Safari visual evidence confirmed the connected
vertical run and displayed the runtime badge `Mongol AI Engine · 原生竖排`.

These focused passes do not convert the untested mobile or Gecko rows into
passes, and they do not replace native-language glyph review.

## Required checks

| Check | Expected outcome | Required evidence |
|---|---|---|
| Official landing page | One clear primary action; no clipping or horizontal overflow | full viewport screenshot |
| Empty composer | Label, warning, input, actions and keyboard are visible and focusable | screenshot + keyboard notes |
| Virtual keyboard input | Character inserts at the current caret without replacing unrelated text | before/after text record |
| Physical keyboard input | Native text entry and Enter/Shift+Enter behavior work | interaction notes |
| Rule response | User and response columns flow top-to-bottom and progress left-to-right | screenshot |
| Long text | Text wraps to additional vertical columns without overlap | screenshot |
| Standard FVS sample | Sequence remains intact; desired glyph is compared with expert reference | screenshot + case ID + font |
| NNBSP suffix sample | U+202F is preserved during input, selection and copy | code-point record + screenshot |
| MVS sample | U+180E is preserved during input, selection and copy | code-point record + screenshot |
| Selection and caret | Selection, deletion and caret movement do not split controls unexpectedly | interaction notes |
| 200% zoom | Core workflow remains operable without two-dimensional page scrolling | screenshot |
| Keyboard-only path | All controls have visible focus and can be reached in a logical order | focus-order notes |

## Result record

For each environment create a JSON review record based on `data/quality/review-record.example.json` and include:

- environment ID and exact versions;
- test case IDs;
- pass, fail, blocked or uncertain result for every required check;
- screenshot paths;
- font name and version;
- reviewer ID and timestamp;
- issue link for every failure.

A browser family is not considered supported until all blocking checks pass in a recorded run. A screenshot from one browser must not be reused as evidence for another.
