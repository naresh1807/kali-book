import http from "node:http";

function inspect(port) {
  return new Promise((resolve, reject) => {
    const request = http.request({hostname:"127.0.0.1", port, path:"/", method:"HEAD", maxHeaderSize:16384}, response => {
      const names = ["content-type", "content-security-policy", "x-content-type-options"];
      const headers = Object.fromEntries(names.map(name => [name, response.headers[name] ?? null]));
      response.resume();
      resolve({status:response.statusCode, headers});
    });
    const timer = setTimeout(() => request.destroy(new Error("Three-second deadline exceeded")), 3000);
    request.on("close", () => clearTimeout(timer));
    request.on("error", reject);
    request.end();
  });
}

try {
  if (process.argv.length > 3) throw new Error("Usage: node local_headers.mjs [port]");
  const raw = process.argv[2] ?? "8877";
  if (!/^[0-9]+$/.test(raw)) throw new Error("Port must contain digits");
  const port = Number(raw);
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error("Port must be 1..65535");
  console.log(JSON.stringify(await inspect(port)));
} catch (error) {
  console.error(`Cannot inspect: ${error.message}`);
  process.exitCode = 1;
}
