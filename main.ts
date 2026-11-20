// main.ts — Validate entry.png against the bounty gate and copy it to the
// output directory. Deterministic, no network, standard library only.
//
// Usage:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The output directory defaults to /output when MAKEFUN_OUTPUT_DIR is unset.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1048576; // 1 MiB
const MAX_DIMENSION = 1024; // pixels
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function fail(message: string): never {
  console.error(`main.ts: error: ${message}`);
  process.exit(1);
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(scriptDir, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const destPath = join(outputDir, "entry.png");

if (!existsSync(sourcePath)) {
  fail(`entry.png not found at ${sourcePath}`);
}

const png = readFileSync(sourcePath);

if (png.length > MAX_BYTES) {
  fail(`entry.png is ${png.length} bytes, over the 1 MiB (${MAX_BYTES}) limit`);
}

if (png.length < 33) {
  fail(`entry.png is only ${png.length} bytes, too small to be a valid PNG`);
}

for (let i = 0; i < PNG_SIGNATURE.length; i++) {
  if (png[i] !== PNG_SIGNATURE[i]) {
    fail("entry.png does not start with the PNG magic bytes");
  }
}

// IHDR chunk: 8-byte signature, 4-byte length, 4-byte "IHDR" type, then the
// width (4 bytes, big-endian) at offset 16 and the height at offset 20.
const chunkType = png.toString("ascii", 12, 16);
if (chunkType !== "IHDR") {
  fail(`first PNG chunk is "${chunkType}", expected "IHDR"`);
}

const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);

if (width === 0 || height === 0) {
  fail(`PNG dimensions must be non-zero, got ${width}x${height}`);
}

if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  fail(`PNG is ${width}x${height}, over the ${MAX_DIMENSION}x${MAX_DIMENSION} limit`);
}

// The file must end with a well-formed IEND chunk (12 bytes: zero length,
// "IEND" type, and the fixed CRC 0xAE426082). This catches truncated files
// that otherwise pass the header checks above.
const IEND_CHUNK = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
if (!png.subarray(png.length - 12).equals(IEND_CHUNK)) {
  fail("entry.png does not end with a valid IEND chunk (file may be truncated)");
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(destPath, png);
console.log(`main.ts: wrote ${png.length} bytes (${width}x${height}) to ${destPath}`);
