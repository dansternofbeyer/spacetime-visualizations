#!/usr/bin/env node
/*
 * check_physics.mjs — runs the physics self-tests embedded in a standalone HTML page.
 *
 * The page keeps all physics between the markers
 *   // ===== PHYSICS CORE START =====   and   // ===== PHYSICS CORE END =====
 * and defines PhysicsCore and PhysicsSelfTests there (see references/selftest-pattern.md).
 * This script extracts that block, runs it in an isolated Node context with only Math
 * available, runs each test, and checks each test's literal `expected` value against
 * physics/reference-values.json when the test names a `refKey`.
 *
 * Usage:
 *   node check_physics.mjs <page.html> [--reference <reference-values.json>]
 * Exit status: 0 when everything passes, 1 otherwise.
 */

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

// ===== Settings =====

const CORE_START_MARKER = "// ===== PHYSICS CORE START =====";
const CORE_END_MARKER = "// ===== PHYSICS CORE END =====";
// How closely a test's literal `expected` must match the generated reference value.
const REFERENCE_MATCH_TOLERANCE = 1e-6;

// ===== Command line =====

function readArguments() {
  const argumentsList = process.argv.slice(2);
  const pagePath = argumentsList.find((argument) => !argument.startsWith("--"));
  if (!pagePath) {
    console.error("Usage: node check_physics.mjs <page.html> [--reference <reference-values.json>]");
    process.exit(1);
  }
  const referenceFlagIndex = argumentsList.indexOf("--reference");
  const referencePath = referenceFlagIndex >= 0
    ? argumentsList[referenceFlagIndex + 1]
    : findDefaultReferenceFile(path.dirname(path.resolve(pagePath)));
  return { pagePath, referencePath };
}

/** Looks for physics/reference-values.json in the page's folder and its parents. */
function findDefaultReferenceFile(startFolder) {
  let folder = startFolder;
  while (true) {
    const candidate = path.join(folder, "physics", "reference-values.json");
    if (fs.existsSync(candidate)) return candidate;
    const parent = path.dirname(folder);
    if (parent === folder) return null;
    folder = parent;
  }
}

// ===== Loading the physics core =====

function extractPhysicsCore(pageText, pagePath) {
  const start = pageText.indexOf(CORE_START_MARKER);
  const end = pageText.indexOf(CORE_END_MARKER);
  if (start < 0 || end < 0 || end < start) {
    throw new Error(`${pagePath}: physics core markers not found (see selftest-pattern.md)`);
  }
  return pageText.slice(start, end);
}

function loadPhysicsCore(coreSource) {
  // Only Math is provided, so any use of the DOM or three.js inside the core fails loudly.
  const sandbox = vm.createContext({ Math, Number, Infinity, NaN, isFinite });
  const script = new vm.Script(`${coreSource}\n;({ PhysicsCore, PhysicsSelfTests })`);
  return script.runInContext(sandbox, { timeout: 10_000 });
}

// ===== Running the tests =====

function relativeError(actual, expected) {
  if (expected === 0) return Math.abs(actual);
  return Math.abs(actual - expected) / Math.abs(expected);
}

function runTest(test, referenceValues) {
  const problems = [];
  let actualValue;
  try {
    actualValue = test.actual();
  } catch (error) {
    return { name: test.name, passed: false, detail: `threw ${error.message}` };
  }
  const error = relativeError(actualValue, test.expected);
  if (!(error <= test.relativeTolerance)) {
    problems.push(`got ${actualValue}, expected ${test.expected} (rel. err ${error.toExponential(2)} > ${test.relativeTolerance})`);
  }
  if (test.refKey) {
    const reference = referenceValues?.[test.refKey];
    if (!reference) {
      problems.push(`refKey "${test.refKey}" not found in reference values`);
    } else if (relativeError(test.expected, reference.value) > Math.max(REFERENCE_MATCH_TOLERANCE, test.relativeTolerance)) {
      problems.push(`expected ${test.expected} is out of date: reference "${test.refKey}" is ${reference.value}`);
    }
  }
  if (!test.source) problems.push("no source given");
  const detail = problems.length ? problems.join("; ") : `${actualValue.toPrecision(10)} (rel. err ${error.toExponential(2)})`;
  return { name: test.name, passed: problems.length === 0, detail };
}

// ===== Main =====

function main() {
  const { pagePath, referencePath } = readArguments();
  const pageText = fs.readFileSync(pagePath, "utf8");
  const { PhysicsSelfTests } = loadPhysicsCore(extractPhysicsCore(pageText, pagePath));
  const referenceValues = referencePath ? JSON.parse(fs.readFileSync(referencePath, "utf8")).values : null;
  if (!referenceValues) console.warn("warning: no physics/reference-values.json found; refKeys can't be checked");

  const results = PhysicsSelfTests.map((test) => runTest(test, referenceValues));
  for (const result of results) console.log(`${result.passed ? "PASS" : "FAIL"}  ${result.name}: ${result.detail}`);
  const failures = results.filter((result) => !result.passed).length;
  console.log(`\n${results.length - failures}/${results.length} passed`);
  process.exit(failures === 0 && results.length > 0 ? 0 : 1);
}

main();
