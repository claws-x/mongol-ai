const JOINING_CONTEXTS = Object.freeze({
    isolate: ["", ""],
    initial: ["", "\u200D"],
    medial: ["\u200D", "\u200D"],
    final: ["\u200D", ""],
});

const VARIATION_SELECTORS = /[\u180B-\u180D\u180F]/gu;

function contextualize(text, context) {
    const pair = JOINING_CONTEXTS[context];
    if (!pair) throw new Error(`Unknown joining context: ${context}`);
    return `${pair[0]}${text}${pair[1]}`;
}

function significantGlyphs(shapeResult) {
    return shapeResult.glyphs.filter((glyph) => !glyph.controlArtifact && (glyph.path.length > 0 || Math.abs(glyph.xAdvance) + Math.abs(glyph.yAdvance) > 0));
}

function glyphFingerprint(shapeResult) {
    return significantGlyphs(shapeResult)
        .map((glyph) => `${glyph.id}:${glyph.xAdvance}:${glyph.yAdvance}:${glyph.xOffset}:${glyph.yOffset}`)
        .join("|");
}

function shapeText(engine, text) {
    return engine.shape(engine.createDocument(text, "unicode-national"));
}

function evaluateStandardizedVariant(engine, task) {
    const validContexts = new Set(task.expected.shaping_contexts);
    const defaultText = task.text.replace(VARIATION_SELECTORS, "");
    const contexts = validContexts.size ? Object.keys(JOINING_CONTEXTS) : ["isolate"];
    const probes = contexts.map((context) => {
        const target = shapeText(engine, contextualize(task.text, context));
        const baseline = shapeText(engine, contextualize(defaultText, context));
        const targetFingerprint = glyphFingerprint(target);
        const defaultFingerprint = glyphFingerprint(baseline);
        const changed = targetFingerprint !== defaultFingerprint;
        const inScope = !validContexts.size || validContexts.has(context);
        const targetGlyphs = significantGlyphs(target);
        const defaultGlyphs = significantGlyphs(baseline);
        const suspectedVisibleSelector = targetGlyphs.length > defaultGlyphs.length;
        let result = "outside_declared_context";
        if (inScope) result = changed && !suspectedVisibleSelector ? "aligned" : suspectedVisibleSelector ? "visible_selector_artifact" : "missing_variant_response";
        return {
            context,
            expectation_class: inScope ? "normative_target" : "outside_declared_context",
            observed_change: changed,
            result,
            target_glyph_ids: targetGlyphs.map((glyph) => glyph.id),
            default_glyph_ids: defaultGlyphs.map((glyph) => glyph.id),
        };
    });
    const scored = probes.filter((probe) => probe.expectation_class === "normative_target");
    const aligned = scored.filter((probe) => probe.result === "aligned").length;
    return {
        method: "unicode-contextual-variant-response",
        scope: "mechanical_standard_alignment_not_linguistic_truth",
        desired_appearance: task.expected.desired_appearance,
        probes,
        score: aligned / scored.length,
        verdict: aligned === scored.length ? "machine_aligned" : "machine_conflict",
    };
}

function evaluateBaseCharacter(engine, task) {
    const probes = Object.keys(JOINING_CONTEXTS).map((context) => {
        const result = shapeText(engine, contextualize(task.text, context));
        const glyphs = significantGlyphs(result);
        return {
            context,
            result: glyphs.length ? "covered" : "missing_visible_glyph",
            glyph_ids: glyphs.map((glyph) => glyph.id),
        };
    });
    const covered = probes.filter((probe) => probe.result === "covered").length;
    return {
        method: "four-context-font-coverage",
        scope: "mechanical_coverage_not_shape_correctness",
        probes,
        score: covered / probes.length,
        verdict: covered === probes.length ? "machine_covered" : "machine_conflict",
    };
}

function evaluateFormatControl(engine, task) {
    if (task.expected.standalone_behavior === "format control requires contextual review") {
        return {
            method: "context-required-format-control",
            scope: "mechanical_control_behavior",
            probes: [{ context: "standalone", result: "needs_context", glyph_ids: [] }],
            score: 0,
            verdict: "needs_context",
        };
    }
    const result = shapeText(engine, task.text);
    const visible = significantGlyphs(result);
    const ignored = visible.length === 0;
    return {
        method: "standalone-format-control-visibility",
        scope: "mechanical_control_behavior",
        probes: [{ context: "standalone", result: ignored ? "ignored_as_expected" : "unexpected_visible_glyph", glyph_ids: visible.map((glyph) => glyph.id) }],
        score: ignored ? 1 : 0,
        verdict: ignored ? "machine_aligned" : "machine_conflict",
    };
}

export function evaluateCorrectnessTask(engine, task) {
    if (task.category === "standardized_variation_sequence") return evaluateStandardizedVariant(engine, task);
    if (task.category === "base_character") return evaluateBaseCharacter(engine, task);
    if (task.category === "format_control") return evaluateFormatControl(engine, task);
    return { method: "unsupported", scope: "none", probes: [], score: 0, verdict: "needs_resolution" };
}

export { JOINING_CONTEXTS, contextualize, glyphFingerprint, significantGlyphs };
