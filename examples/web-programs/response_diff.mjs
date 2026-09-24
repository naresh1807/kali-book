import {open} from "node:fs/promises";
import {createHash} from "node:crypto";
async function load(path) {
  const file=await open(path,"r"), buffer=Buffer.alloc(1048577);let used=0;
  try {while(used<buffer.length) {const {bytesRead}=await file.read(buffer,used,buffer.length-used,null);if(!bytesRead)break;used+=bytesRead;}}
  finally {await file.close();}
  if(used>1048576)throw new Error("File too large");
  const row=JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(buffer.subarray(0,used)));
  if(!row || Array.isArray(row) || !Number.isInteger(row.status) || row.status<100 || row.status>599 || typeof row.body!=="string")throw new Error("Invalid response shape");
  return row;
}
try {
  if(process.argv.length!==4)throw new Error("Usage: node response_diff.mjs baseline.json comparison.json");
  const a=await load(process.argv[2]),b=await load(process.argv[3]);
  console.log(JSON.stringify({same_status:a.status===b.status,same_body:a.body===b.body,body_bytes:[a,b].map(x=>Buffer.byteLength(x.body,"utf8")),sha256:[a,b].map(x=>createHash("sha256").update(x.body,"utf8").digest("hex")),note:"Different responses do not prove broken authorization. Verify identity, expected permissions and returned data."}));
} catch {console.error("Cannot compare: invalid or unreadable input");process.exitCode=1;}
