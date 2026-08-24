#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { pathToFileURL } from "node:url";
import { buildCorpusDocument } from "../../core/web_corpus.mjs";

const USER_AGENT = "MongolAI-CorpusBot/0.1 (+https://github.com/claws-x/mongol-ai; research corpus; contact via GitHub issues)";

function parseArgs(argv) {
    const result = { sources: "data/corpus/sources.json", output: "data/corpus/observations.json", sourceId: null, delayMs: 1500 };
    for (let index = 0; index < argv.length; index += 1) {
        const key = argv[index];
        const value = argv[index + 1];
        if (key === "--sources") result.sources = value;
        else if (key === "--output") result.output = value;
        else if (key === "--source") result.sourceId = value;
        else if (key === "--delay-ms") result.delayMs = Number(value);
        else throw new Error(`unknown argument: ${key}`);
        index += 1;
    }
    if (!Number.isFinite(result.delayMs) || result.delayMs < 500) throw new Error("--delay-ms must be at least 500");
    return result;
}

export function parseRobots(text, userAgent = USER_AGENT) {
    const groups = [];
    let current = null;
    for (const rawLine of text.split(/\r?\n/u)) {
        const line = rawLine.replace(/#.*$/u, "").trim();
        if (!line) continue;
        const separator = line.indexOf(":");
        if (separator < 0) continue;
        const field = line.slice(0, separator).trim().toLowerCase();
        const value = line.slice(separator + 1).trim();
        if (field === "user-agent") {
            if (!current || current.rules.length) {
                current = { agents: [], rules: [] };
                groups.push(current);
            }
            current.agents.push(value.toLowerCase());
        } else if (current && (field === "allow" || field === "disallow")) {
            current.rules.push({ type: field, path: value });
        }
    }
    const agent = userAgent.toLowerCase().split("/")[0];
    const matching = groups.filter((group) => group.agents.some((candidate) => candidate === "*" || agent.includes(candidate)));
    return matching.flatMap((group) => group.rules);
}

export function robotsAllows(url, rules) {
    const parsed = new URL(url);
    const pathname = `${parsed.pathname || "/"}${parsed.search}`;
    const matchesRule = (path) => {
        const anchored = path.endsWith("$");
        const body = anchored ? path.slice(0, -1) : path;
        const expression = body
            .replace(/[.+?^${}()|[\]\\]/gu, "\\$&")
            .replace(/\*/gu, ".*");
        return new RegExp(`^${expression}${anchored ? "$" : ""}`, "u").test(pathname);
    };
    const matches = rules
        .filter((rule) => rule.path && matchesRule(rule.path))
        .sort((a, b) => b.path.length - a.path.length);
    return matches.length === 0 || matches[0].type === "allow";
}

async function fetchRobots(url) {
    const origin = new URL(url).origin;
    const response = await fetch(`${origin}/robots.txt`, { headers: { "user-agent": USER_AGENT }, redirect: "follow" });
    if (response.status === 404) return [];
    if (!response.ok) throw new Error(`robots check failed with HTTP ${response.status} for ${origin}`);
    return parseRobots(await response.text());
}

async function crawlSource(source, delayMs) {
    if (source.enabled !== true) return [];
    const documents = [];
    for (const [index, url] of source.seedUrls.entries()) {
        const rules = await fetchRobots(url);
        if (!robotsAllows(url, rules)) {
            console.warn(`robots denied ${url}`);
            continue;
        }
        if (index > 0) await delay(delayMs);
        const response = await fetch(url, {
            headers: { "accept": "text/html,application/xhtml+xml", "user-agent": USER_AGENT },
            redirect: "follow",
        });
        if (!response.ok) throw new Error(`HTTP ${response.status} for ${url}`);
        const contentType = response.headers.get("content-type") ?? "";
        if (!contentType.includes("text/html") && !contentType.includes("application/xhtml+xml")) {
            throw new Error(`unsupported content type ${contentType} for ${url}`);
        }
        const html = await response.text();
        const document = buildCorpusDocument({ source, sourceUrl: response.url, fetchedAt: new Date().toISOString(), html });
        documents.push(document);
        console.log(`${source.id}: ${document.segmentCount} segments from ${response.url}`);
    }
    return documents;
}

async function main() {
    const args = parseArgs(process.argv.slice(2));
    const sourcePayload = JSON.parse(fs.readFileSync(args.sources, "utf8"));
    const selected = sourcePayload.sources.filter((source) => !args.sourceId || source.id === args.sourceId);
    if (!selected.length) throw new Error(`no matching source: ${args.sourceId ?? "enabled sources"}`);
    const documents = [];
    const failures = [];
    for (const [index, source] of selected.entries()) {
        if (index > 0) await delay(args.delayMs);
        try {
            documents.push(...await crawlSource(source, args.delayMs));
        } catch (error) {
            const code = error?.cause?.code ?? error?.code ?? "CRAWL_ERROR";
            failures.push({ sourceId: source.id, code, message: String(error?.message ?? error) });
            console.warn(`${source.id}: ${code} ${error?.message ?? error}`);
        }
    }
    const payload = {
        schemaVersion: "1.0.0",
        generatedAt: new Date().toISOString(),
        scope: "short-public-web-text-observations-not-redistributable-articles",
        documents,
        failures,
    };
    fs.mkdirSync(path.dirname(args.output), { recursive: true });
    fs.writeFileSync(args.output, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
    console.log(`wrote ${documents.length} documents to ${args.output}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) main();
