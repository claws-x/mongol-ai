import assert from "node:assert/strict";
import test from "node:test";

import { buildControlCooccurrenceIndex, buildCorpusDocument, buildCorpusStats, htmlToText } from "../../core/web_corpus.mjs";
import { parseRobots, robotsAllows } from "../../tools/corpus/crawl.mjs";

const source = {
    id: "fixture",
    language: "mn-Mong",
    license: "test-fixture",
    redistributable: false,
};

test("HTML extraction preserves exact Mongolian controls while excluding scripts", () => {
    const html = "<html><body><p>Prefix &amp; ᠮᠣᠩᠭᠣᠯ ᠤ</p><script>ᠪᠤᠷᠤᠭᠤ</script><p>ᠠ&#x180C;</p></body></html>";
    const text = htmlToText(html);
    assert.match(text, /ᠮᠣᠩᠭᠣᠯ ᠤ/u);
    assert.match(text, /ᠠ᠌/u);
    assert.doesNotMatch(text, /ᠪᠤᠷᠤᠭᠤ/u);
    const document = buildCorpusDocument({ source, sourceUrl: "https://example.test/page", fetchedAt: "2026-08-24T00:00:00.000Z", html });
    assert.equal(document.segmentCount, 2);
    assert.deepEqual(document.segments.flatMap((segment) => segment.controls), ["U+202F", "U+180C"]);
    assert.equal(document.segments.map((segment) => segment.text).join("").includes("ᠠ᠌"), true);
});

test("corpus statistics count code points and domains without shaping guesses", () => {
    const first = buildCorpusDocument({ source, sourceUrl: "https://one.test/", fetchedAt: "2026-08-24T00:00:00.000Z", html: "<p>ᠠ᠌</p>" });
    const second = buildCorpusDocument({ source, sourceUrl: "https://two.test/", fetchedAt: "2026-08-24T00:00:00.000Z", html: "<p>ᠠ</p>" });
    const stats = buildCorpusStats([first, second]);
    assert.equal(stats.domainCount, 2);
    assert.equal(stats.codepoints["U+1820"], 2);
    assert.equal(stats.controls["U+180C"], 1);
    assert.equal(stats.scope, "raw-codepoint-and-context-observation-not-linguistic-truth");
});

test("control cooccurrence index stores codepoint context and zero-count controls honestly", () => {
    const first = buildCorpusDocument({
        source,
        sourceUrl: "https://one.test/",
        fetchedAt: "2026-08-24T00:00:00.000Z",
        html: "<p>ᠮᠣᠩᠭᠣᠯ᠎ᠳᠤᠷ ᠠ᠌</p>",
    });
    const second = buildCorpusDocument({
        source,
        sourceUrl: "https://two.test/",
        fetchedAt: "2026-08-24T00:00:00.000Z",
        html: "<p>ᠮᠣᠩᠭᠣᠯ ᠳᠤᠷ</p>",
    });
    const index = buildControlCooccurrenceIndex([first, second]);
    assert.equal(index.scope, "codepoint-cooccurrence-observation-not-word-or-glyph-truth");
    assert.equal(index.observedControls["U+180E"], 1);
    assert.equal(index.observedControls["U+202F"], 1);
    assert.equal(index.observedControls["U+180C"], 1);
    assert.equal(index.observedControls["U+200D"], 0);
    assert.equal(index.records.length, 3);
    assert.ok(index.records.every((record) => record.leftSequence.every((label) => label.startsWith("U+"))));
    assert.ok(index.records.every((record) => !("text" in record)));
});

test("robots rules use longest matching path and never ignore disallow", () => {
    const rules = parseRobots("User-agent: *\nDisallow: /private\nAllow: /private/public\nDisallow: /*?download=$\n");
    assert.equal(robotsAllows("https://example.test/private/data", rules), false);
    assert.equal(robotsAllows("https://example.test/private/public/page", rules), true);
    assert.equal(robotsAllows("https://example.test/open", rules), true);
    assert.equal(robotsAllows("https://example.test/file?download=", rules), false);
});
