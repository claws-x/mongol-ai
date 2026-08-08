import assert from "node:assert/strict";
import fs from "node:fs";
import { test } from "node:test";
import * as hb from "harfbuzzjs";
import { LosslessMongolianDocument, MongolianSuperEngine, PROFILES, LOCKED_FONT_SHA256 } from "../../core/mongolian_super_engine.mjs";

test("lossless documents preserve controls and spaces exactly", () => {
    const input = "ᠪᠠᠶᠢᠨ\u180Eᠤ\u202Fᠤ";
    const document = new LosslessMongolianDocument(input, "onon-mn");
    assert.equal(document.serialize(), input);
    assert.deepEqual(document.diagnostics().controls.map((token) => token.control), ["MVS", "NNBSP"]);
    assert.equal(document.diagnostics().roundTripExact, true);
});

test("private encoding profiles are preserved but never guessed", () => {
    const input = "\uE234\uE235";
    const document = new LosslessMongolianDocument(input, "onon-mk");
    assert.equal(document.serialize(), input);
    assert.equal(document.diagnostics().canShape, false);
    assert.equal(document.diagnostics().pua.length, 2);
    assert.ok(document.diagnostics().issues.some((issue) => issue.code === "authoritative-mapping-required"));
});

test("all declared profiles carry evidence and a no-guess boundary", () => {
    for (const profile of Object.values(PROFILES)) {
        assert.match(profile.evidence, /^https:\/\//);
        assert.ok(profile.note.length > 10);
    }
});

test("locked HarfBuzz and font produce the recorded shaping fingerprint", () => {
    const fontBytes = fs.readFileSync(new URL("../../assets/fonts/NotoSansMongolian-Regular.ttf", import.meta.url));
    const blob = new hb.Blob(fontBytes);
    const face = new hb.Face(blob);
    const font = new hb.Font(face);
    const buffer = new hb.Buffer();
    buffer.addText("ᠮᠣᠩᠭᠣᠯ");
    buffer.setDirection(hb.Direction.LTR);
    buffer.setScript("Mong");
    buffer.setLanguage("mn");
    buffer.setFlags(hb.BufferFlag.PRESERVE_DEFAULT_IGNORABLES);
    hb.shape(font, buffer);
    assert.equal(hb.versionString(), "14.3.0");
    assert.deepEqual(buffer.getGlyphInfos().map((glyph) => glyph.codepoint), [121, 32, 1299, 32, 129]);
    assert.equal(LOCKED_FONT_SHA256.length, 64);
});

test("rejected Pages phrase is not an approved override", () => {
    const payload = JSON.parse(fs.readFileSync(new URL("../../data/engine/glyph-overrides.json", import.meta.url), "utf8"));
    assert.deepEqual(payload.overrides, []);
});

test("web workbench respects native IME composition boundaries", () => {
    const script = fs.readFileSync(new URL("../../engine/engine-lab.mjs", import.meta.url), "utf8");
    const html = fs.readFileSync(new URL("../../engine/index.html", import.meta.url), "utf8");
    for (const eventName of ["compositionstart", "compositionupdate", "compositionend", "beforeinput", "input"]) {
        assert.ok(script.includes(eventName), `${eventName} handler is required`);
    }
    assert.ok(script.includes("if (!isComposing && !event.isComposing) run()"));
    assert.ok(script.includes("browserCannotIdentifySystemIme: true"));
    assert.ok(html.includes("导出输入证据 JSON"));
    assert.doesNotMatch(html, /<textarea[^>]*>[^<]+<\/textarea>/);
});

test("captured user sample has an exact non-linguistic renderer fingerprint", () => {
    const payload = JSON.parse(fs.readFileSync(new URL("../../data/quality/mongolian-rendering-goldens.json", import.meta.url), "utf8"));
    const sample = payload.cases.find((item) => item.id === "user-captured-chat-sample-2026-08-08");
    assert.equal(sample.text, "ᠦᠷᠭᠥᠯᠵᠢᠯ");
    assert.deepEqual(sample.code_points, ["U+1826", "U+1837", "U+182D", "U+1825", "U+182F", "U+1835", "U+1822", "U+182F"]);
    assert.deepEqual(sample.glyph_ids, [58, 176, 964, 128, 163, 26, 129]);
    assert.equal(sample.review.linguistic_correctness, "unreviewed");
    assert.equal(sample.review.input_method, "not_yet_confirmed");
});

test("session reference fonts shape locally and expose glyph trace attributes", async () => {
    const fontBytes = fs.readFileSync(new URL("../../assets/fonts/NotoSansMongolian-Regular.ttf", import.meta.url));
    const engine = new MongolianSuperEngine({ expectedFontHash: null });
    const report = await engine.initFromFontBytes(fontBytes, { expectedHash: null, overrides: [] });
    assert.equal(report.ready, true);
    assert.equal(report.fontLocked, false);
    const result = engine.shape(engine.createDocument("ᠦᠷᠭᠥᠯᠵᠢᠯ", "unicode-national"));
    assert.equal(result.status, "shaped");
    const svg = engine.renderSvg(result);
    assert.match(svg, /data-glyph-index="0"/);
    assert.match(svg, /data-glyph-id="\d+"/);
    assert.match(svg, /data-cluster="\d+"/);
});
