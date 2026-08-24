#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const [, , queuePath, matrixPath, evidencePath, outputPath] = process.argv;
if (!queuePath || !matrixPath || !evidencePath || !outputPath) {
    throw new Error("usage: node scripts/build_s2_semantic_registry.mjs REVIEW_QUEUE CONTEXT_MATRIX MACHINE_EVIDENCE OUTPUT");
}

const queue = JSON.parse(fs.readFileSync(queuePath, "utf8"));
const matrix = JSON.parse(fs.readFileSync(matrixPath, "utf8"));
const evidence = JSON.parse(fs.readFileSync(evidencePath, "utf8"));
const tasks = new Map(queue.tasks.map((task) => [task.id, task]));
const observations = new Map(evidence.results.map((result) => [result.task_id, result]));

function slugBase(name) {
    return name.replace(/^MONGOLIAN LETTER /u, "MONGOLIAN_").replace(/[^A-Z0-9]+/gu, "_").replace(/^_|_$/gu, "");
}

function formId(description) {
    const match = /^(second|third|fourth) form$/u.exec(description);
    const ordinals = { second: 2, third: 3, fourth: 4 };
    if (!match) throw new Error(`unsupported desired appearance: ${description}`);
    return `form${ordinals[match[1]]}`;
}

const targets = matrix.probes
    .filter((probe) => probe.expectation_class === "normative_target")
    .map((probe) => {
        const task = tasks.get(probe.task_id);
        const observationContext = probe.context === "context_independent" ? "isolate" : probe.context;
        const observation = observations.get(probe.task_id)?.probes.find((item) => item.context === observationContext);
        if (!task || !observation) throw new Error(`missing task or observation for ${probe.id}`);
        const base = slugBase(task.expected.base_character);
        const form = formId(task.expected.desired_appearance);
        const joiningState = probe.context === "context_independent" ? "any" : probe.context;
        const semanticRole = `${base}.${joiningState}.${form}`;
        const backendStatus = observation.result === "aligned" ? "supported" : "project-glyph-required";
        return {
            id: `s2-role-${probe.task_id.slice(-3)}-${probe.context}`,
            semanticRole,
            character: task.expected.base_character,
            baseCodePoint: task.code_points[0],
            selectorCodePoint: task.code_points[1],
            inputSequence: task.code_points,
            joiningState,
            variationIntent: form,
            desiredAppearance: task.expected.desired_appearance,
            source: task.source,
            ruleStatus: "unicode-declared-target",
            backend: {
                id: "noto-sans-mongolian-3.002-harfbuzz-14.3.0",
                status: backendStatus,
                observation: observation.result,
                targetGlyphIds: observation.target_glyph_ids,
                defaultGlyphIds: observation.default_glyph_ids,
            },
        };
    });

if (targets.length !== 93) throw new Error(`expected 93 semantic targets, found ${targets.length}`);
if (new Set(targets.map((target) => target.id)).size !== targets.length) throw new Error("duplicate semantic target id");
if (new Set(targets.map((target) => `${target.inputSequence.join(" ")}|${target.joiningState}`)).size !== targets.length) {
    throw new Error("duplicate input sequence and joining state");
}

const byBackendStatus = Object.fromEntries(
    [...new Set(targets.map((target) => target.backend.status))]
        .sort()
        .map((status) => [status, targets.filter((target) => target.backend.status === status).length]),
);

const payload = {
    schemaVersion: "1.0.0",
    generatedAt: queue.generated_at,
    phase: "S2",
    scope: "semantic-role registry derived from Unicode-declared contexts plus locked-backend observation",
    summary: {
        targetCount: targets.length,
        semanticRoleCount: new Set(targets.map((target) => target.semanticRole)).size,
        byBackendStatus,
    },
    targets,
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
console.log(`wrote ${targets.length} semantic targets to ${outputPath}`);
