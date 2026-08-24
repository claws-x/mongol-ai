import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const corePath = resolve(root, "core/mongolian_super_engine.mjs");
const vendorDir = resolve(root, "assets/vendor/harfbuzzjs");
const manifest = JSON.parse(await readFile(resolve(vendorDir, "manifest.json"), "utf8"));
const core = await readFile(corePath, "utf8");

if (/from\s+["'][^"']*node_modules\//.test(core)) {
    throw new Error("Production engine imports node_modules, which GitHub Pages does not publish.");
}
if (!core.includes('../assets/vendor/harfbuzzjs/index.mjs')) {
    throw new Error("Production engine is not wired to the vendored HarfBuzz runtime.");
}

for (const [name, expected] of Object.entries(manifest.files)) {
    const bytes = await readFile(resolve(vendorDir, name));
    const actual = createHash("sha256").update(bytes).digest("hex");
    if (actual !== expected) throw new Error(`${name}: SHA-256 mismatch`);
}

console.log(`Pages runtime verified: ${manifest.package}@${manifest.version}, ${Object.keys(manifest.files).length} locked files.`);
