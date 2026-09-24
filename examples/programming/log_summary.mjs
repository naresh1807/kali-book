import {open} from "node:fs/promises";

async function summarize(path) {
  const handle = await open(path, "r");
  const buffer = Buffer.alloc(1_048_577);
  let used = 0;
  try {
    while (used < buffer.length) {
      const {bytesRead} = await handle.read(buffer, used, buffer.length - used, null);
      if (!bytesRead) break;
      used += bytesRead;
    }
  } finally { await handle.close(); }
  if (used > 1_048_576) throw new Error("Input exceeds 1 MiB");
  const text = new TextDecoder("utf-8", {fatal:true}).decode(buffer.subarray(0, used));
  const counts = new Map();
  let records = 0;
  for (const [index, line] of text.split(/\r?\n/).entries()) {
    if (!line.trim()) continue;
    const row = JSON.parse(line);
    if (!row || Array.isArray(row) || typeof row !== "object" || !Number.isInteger(row.status) || row.status < 100 || row.status > 599) {
      throw new Error(`Invalid status on line ${index + 1}`);
    }
    const status = String(row.status);
    counts.set(status, (counts.get(status) ?? 0) + 1);
    records += 1;
  }
  return {records, statuses: Object.fromEntries([...counts].sort())};
}

if (process.argv.length !== 3) {
  console.error("Usage: node log_summary.mjs sample.jsonl");
  process.exitCode = 2;
} else {
  try { console.log(JSON.stringify(await summarize(process.argv[2]))); }
  catch (error) { console.error(`Cannot summarize: ${error.message}`); process.exitCode = 1; }
}
