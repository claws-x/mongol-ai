#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const [, , registryPath, outputPath] = process.argv;
if (!registryPath || !outputPath) throw new Error("usage: node scripts/build_s2_geometry_requirements.mjs SEMANTIC_REGISTRY OUTPUT_JSON");

const semantic = JSON.parse(fs.readFileSync(registryPath, "utf8"));
const required = semantic.targets.filter((target) => target.backend.status === "project-glyph-required");
const connectorFlags = (state) => ({
    entry: state === "medial" || state === "final",
    exit: state === "initial" || state === "medial",
});

const payload = {
    schemaVersion: "1.0.0",
    generatedAt: "2026-08-25",
    phase: "S2.2",
    coordinateSystem: {
        name: "logical-font-space-x-forward-y-up",
        flowAxis: "positive-x-before-vertical-rotation",
        verticalMapping: "leading-edge-to-top; trailing-edge-to-bottom",
    },
    licensePolicy: "Only Mongol AI original outlines or explicitly OFL-compatible derived outlines may be registered.",
    summary: {
        requirementCount: required.length,
        assetCount: 0,
        readyCount: 0,
        missingCount: required.length,
    },
    requirements: required.map((target) => ({
        id: `geometry-${target.id}`,
        semanticRole: target.semanticRole,
        semanticTargetId: target.id,
        joiningState: target.joiningState,
        requiredAnchors: connectorFlags(target.joiningState),
        constraints: {
            positiveAdvance: true,
            nonEmptyPath: true,
            nonEmptyBoundingBox: true,
            edgeToleranceEm: 0.02,
            stemAlignmentToleranceEm: 0.04,
            controlGlyphsForbidden: true,
        },
        assetStatus: "missing",
    })),
    assets: [],
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
console.log(`wrote ${payload.summary.requirementCount} geometry requirements; ${payload.summary.assetCount} assets ready`);
