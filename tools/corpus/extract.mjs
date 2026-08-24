#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { buildCorpusDocument } from "../../core/web_corpus.mjs";

function usage() {
    throw new Error("usage: node tools/corpus/extract.mjs SOURCE_JSON HTML_FILE OUTPUT_JSON");
}

const [, , sourcePath, htmlPath, outputPath] = process.argv;
if (!sourcePath || !htmlPath || !outputPath) usage();

const source = JSON.parse(fs.readFileSync(sourcePath, "utf8"));
const html = fs.readFileSync(htmlPath, "utf8");
const sourceUrl = source.seedUrls?.[0];
if (!sourceUrl) throw new Error("source must include at least one seedUrls entry");

const document = buildCorpusDocument({
    source,
    sourceUrl,
    fetchedAt: new Date().toISOString(),
    html,
});
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(document, null, 2)}\n`, "utf8");
console.log(`extracted ${document.segmentCount} Mongolian segments from ${sourceUrl}`);
