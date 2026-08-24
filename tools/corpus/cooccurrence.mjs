#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { buildControlCooccurrenceIndex } from "../../core/web_corpus.mjs";

const [, , inputPath, outputPath] = process.argv;
if (!inputPath || !outputPath) throw new Error("usage: node tools/corpus/cooccurrence.mjs OBSERVATIONS_JSON OUTPUT_JSON");

const payload = JSON.parse(fs.readFileSync(inputPath, "utf8"));
if (!Array.isArray(payload.documents)) throw new Error("input must contain documents[]");
const index = buildControlCooccurrenceIndex(payload.documents);
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(index, null, 2)}\n`, "utf8");
console.log(`wrote ${index.recordCount} control cooccurrence records from ${index.documentCount} documents`);
