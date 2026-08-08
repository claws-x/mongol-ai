import assert from "node:assert/strict";
import fs from "node:fs";
import { test } from "node:test";
import * as hb from "harfbuzzjs";
import { LosslessMongolianDocument, PROFILES, LOCKED_FONT_SHA256 } from "../../core/mongolian_super_engine.mjs";

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
