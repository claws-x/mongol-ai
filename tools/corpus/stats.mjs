#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { buildCorpusStats } from "../../core/web_corpus.mjs";

const [, , inputPath, outputPath] = process.argv;
if (!inputPath || !outputPath) throw new Error("usage: node tools/corpus/stats.mjs DOCUMENTS_JSON OUTPUT_JSON");

const payload = JSON.parse(fs.readFileSync(inputPath, "utf8"));
const documents = Array.isArray(payload) ? payload : payload.documents;
if (!Array.isArray(documents)) throw new Error("input must be an array or an object with documents[]");
const stats = buildCorpusStats(documents);
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(stats, null, 2)}\n`, "utf8");
console.log(`wrote corpus statistics for ${stats.documentCount} documents`);
