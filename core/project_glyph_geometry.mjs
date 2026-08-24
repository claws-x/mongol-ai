const JOINING_STATES = new Set(["isolate", "initial", "medial", "final"]);
const SAFE_SVG_PATH = /^[MmZzLlHhVvCcSsQqTtAaEe0-9+\-.,\s]+$/u;

function finiteNumber(value) {
    return typeof value === "number" && Number.isFinite(value);
}

function requiredConnectors(joiningState) {
    return {
        entry: joiningState === "medial" || joiningState === "final",
        exit: joiningState === "initial" || joiningState === "medial",
    };
}

export function validateProjectGlyphAsset(requirement, asset) {
    const violations = [];
    if (!asset || typeof asset !== "object") return ["asset-missing"];
    if (asset.semanticRole !== requirement.semanticRole) violations.push("semantic-role-mismatch");
    if (!finiteNumber(asset.unitsPerEm) || asset.unitsPerEm <= 0) violations.push("invalid-units-per-em");
    if (!finiteNumber(asset.advance) || asset.advance <= 0) violations.push("non-positive-advance");
    if (typeof asset.path !== "string" || !asset.path.trim()) violations.push("empty-path");
    else if (!SAFE_SVG_PATH.test(asset.path)) violations.push("unsafe-svg-path");

    const box = asset.bbox;
    if (!box || ![box.xMin, box.yMin, box.xMax, box.yMax].every(finiteNumber)) {
        violations.push("invalid-bbox");
    } else if (box.xMin >= box.xMax || box.yMin >= box.yMax) {
        violations.push("empty-bbox");
    }

    const upem = finiteNumber(asset.unitsPerEm) && asset.unitsPerEm > 0 ? asset.unitsPerEm : 1000;
    const edgeTolerance = requirement.constraints.edgeToleranceEm * upem;
    const stemTolerance = requirement.constraints.stemAlignmentToleranceEm * upem;
    const expected = requiredConnectors(requirement.joiningState);
    const entry = asset.anchors?.entry ?? null;
    const exit = asset.anchors?.exit ?? null;

    if (expected.entry && (!entry || !finiteNumber(entry.x) || !finiteNumber(entry.y))) violations.push("missing-entry-anchor");
    if (expected.exit && (!exit || !finiteNumber(exit.x) || !finiteNumber(exit.y))) violations.push("missing-exit-anchor");
    if (!expected.entry && entry !== null) violations.push("unexpected-entry-anchor");
    if (!expected.exit && exit !== null) violations.push("unexpected-exit-anchor");

    if (box && entry && finiteNumber(entry.x) && Math.abs(entry.x - box.xMin) > edgeTolerance) {
        violations.push("entry-not-on-leading-edge");
    }
    if (box && exit && finiteNumber(exit.x) && Math.abs(exit.x - box.xMax) > edgeTolerance) {
        violations.push("exit-not-on-trailing-edge");
    }
    if (entry && exit && finiteNumber(entry.y) && finiteNumber(exit.y) && Math.abs(entry.y - exit.y) > stemTolerance) {
        violations.push("stem-axis-discontinuity");
    }
    if (!asset.source || !["mongol-ai-original", "ofl-derived"].includes(asset.source.kind)) {
        violations.push("unacceptable-outline-source");
    }
    if (!asset.source?.license) violations.push("missing-outline-license");
    return [...new Set(violations)];
}

export class ProjectGlyphGeometryRegistry {
    constructor(payload) {
        if (payload?.schemaVersion !== "1.0.0" || !Array.isArray(payload.requirements) || !Array.isArray(payload.assets)) {
            throw new Error("invalid project glyph geometry registry");
        }
        this.payload = payload;
        this.requirements = new Map();
        this.assets = new Map();
        for (const requirement of payload.requirements) {
            if (!JOINING_STATES.has(requirement.joiningState)) throw new Error(`invalid joining state: ${requirement.joiningState}`);
            if (this.requirements.has(requirement.semanticRole)) throw new Error(`duplicate geometry requirement: ${requirement.semanticRole}`);
            this.requirements.set(requirement.semanticRole, Object.freeze(requirement));
        }
        for (const asset of payload.assets) {
            if (this.assets.has(asset.semanticRole)) throw new Error(`duplicate project glyph asset: ${asset.semanticRole}`);
            this.assets.set(asset.semanticRole, Object.freeze(asset));
        }
    }

    resolve(semanticRole) {
        const requirement = this.requirements.get(semanticRole);
        if (!requirement) return { status: "not-required", semanticRole, requirement: null, asset: null, violations: [] };
        const asset = this.assets.get(semanticRole) ?? null;
        if (!asset) return { status: "asset-missing", semanticRole, requirement, asset: null, violations: ["asset-missing"] };
        const violations = validateProjectGlyphAsset(requirement, asset);
        return {
            status: violations.length ? "asset-invalid" : "asset-ready",
            semanticRole,
            requirement,
            asset,
            violations,
        };
    }
}

export { requiredConnectors };
