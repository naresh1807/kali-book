import http from "node:http";
import https from "node:https";
const LIMIT = 262144;

function request(url, mode) {
  const u = new URL(url);
  if (!["http:", "https:"].includes(u.protocol) || u.username || u.password || u.hash) throw new Error("Invalid URL");
  return new Promise((resolve, reject) => {
    const headers = {"User-Agent":"Kali-Fieldbook-Lab/1.0", "Accept-Encoding":"identity"};
    if (mode === "cors") headers.Origin = "https://review.invalid";
    const req = (u.protocol === "https:" ? https : http).get(u, {headers, maxHeaderSize:16384}, res => {
      let size = 0;
      res.on("data", chunk => {size += chunk.length; if (size > LIMIT) req.destroy(new Error("Body too large"));});
      res.on("error", reject);
      res.on("end", () => {
        if (size > LIMIT) return;
        const values = new Map();
        for (let i=0; i<res.rawHeaders.length; i+=2) {
          const name = res.rawHeaders[i].toLowerCase();
          values.set(name, [...(values.get(name) ?? []), res.rawHeaders[i+1]]);
        }
        resolve({status:res.statusCode, values});
      });
    });
    const timer = setTimeout(() => req.destroy(new Error("Deadline")), 3000);
    req.on("close", () => clearTimeout(timer));
    req.on("error", reject);
  });
}
function analyze(mode, {status, values}) {
  if (mode === "headers") {
    const names = ["content-security-policy","strict-transport-security","x-content-type-options","referrer-policy","x-frame-options"];
    return {status, present:Object.fromEntries(names.map(n => [n,values.has(n)])), note:"Presence is not proof of correct policy; inspect application context."};
  }
  if (mode === "cookies") {
    const cookies = (values.get("set-cookie") ?? []).map(raw => {
      const parts = raw.split(";").map(x => x.trim());
      const separator = parts[0].indexOf("=");
      if (separator < 0) return {parse_error:"Missing cookie name/value separator"};
      const attributes = new Map(parts.slice(1).map(part => {
        const at = part.indexOf("=");
        return at < 0 ? [part.toLowerCase(), ""] : [part.slice(0,at).toLowerCase(), part.slice(at+1)];
      }));
      return {name:parts[0].slice(0,separator), secure:attributes.has("secure"), httponly:attributes.has("httponly"), samesite:attributes.get("samesite") ?? null, domain_attribute:attributes.has("domain")};
    });
    return {status,cookies,note:"Values omitted. Attribute summary is not a full browser cookie-policy validator."};
  }
  const allow_origin = values.get("access-control-allow-origin") ?? [];
  const allow_credentials = values.get("access-control-allow-credentials") ?? [];
  return {status,allow_origin,allow_credentials,review_reflection:allow_origin.length===1 && allow_origin[0]==="https://review.invalid" && allow_credentials.length===1 && allow_credentials[0]==="true",note:"One synthetic Origin probe; browser behavior, credentials and sensitive data must be assessed separately."};
}
const [mode,url] = process.argv.slice(2);
if (process.argv.length !== 4 || !["headers","cookies","cors"].includes(mode)) {
  console.error("Usage: node web_review.mjs headers|cookies|cors URL"); process.exitCode=2;
} else {
  try {console.log(JSON.stringify(analyze(mode,await request(url,mode))));}
  catch {console.error("Review failed: request or input error");process.exitCode=1;}
}
