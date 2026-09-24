import argparse, http.client, json, ssl
from urllib.parse import urlsplit
LIMIT = 262144

def request(url, origin=None):
    u = urlsplit(url)
    if u.scheme not in ("http", "https") or not u.hostname or u.username or u.password or u.fragment:
        raise ValueError("Use an HTTP(S) URL without credentials or fragment")
    port = u.port or (443 if u.scheme == "https" else 80)
    cls = http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection
    connection = cls(u.hostname, port, timeout=3)
    headers = {"User-Agent": "Kali-Fieldbook-Lab/1.0", "Accept-Encoding": "identity"}
    if origin is not None:
        headers["Origin"] = origin
    try:
        connection.request("GET", (u.path or "/") + ("?" + u.query if u.query else ""), headers=headers)
        response = connection.getresponse()
        body = response.read(LIMIT + 1)
        if len(body) > LIMIT:
            raise ValueError("Response exceeds 256 KiB")
        return response.status, response.getheaders()
    finally:
        connection.close()

def analyze(mode, status, headers):
    values = {}
    for name, value in headers:
        values.setdefault(name.lower(), []).append(value)
    if mode == "headers":
        names = ["content-security-policy", "strict-transport-security", "x-content-type-options", "referrer-policy", "x-frame-options"]
        return {"status": status, "present": {n: n in values for n in names}, "note": "Presence is not proof of correct policy; inspect application context."}
    if mode == "cookies":
        result = []
        for raw in values.get("set-cookie", []):
            parts = [part.strip() for part in raw.split(";")]
            if "=" not in parts[0]:
                result.append({"parse_error": "Missing cookie name/value separator"})
                continue
            name = parts[0].split("=", 1)[0]
            attributes = {}
            for part in parts[1:]:
                key, _, value = part.partition("=")
                attributes[key.lower()] = value
            result.append({"name": name, "secure": "secure" in attributes, "httponly": "httponly" in attributes, "samesite": attributes.get("samesite"), "domain_attribute": "domain" in attributes})
        return {"status": status, "cookies": result, "note": "Values omitted. Attribute summary is not a full browser cookie-policy validator."}
    acao = values.get("access-control-allow-origin", [])
    acac = values.get("access-control-allow-credentials", [])
    return {"status": status, "allow_origin": acao, "allow_credentials": acac, "review_reflection": acao == ["https://review.invalid"] and acac == ["true"], "note": "One synthetic Origin probe; browser behavior, credentials and sensitive data must be assessed separately."}

def main():
    p = argparse.ArgumentParser(description="One GET; no redirects; no supplied credentials. Use your approved URL.")
    p.add_argument("mode", choices=["headers", "cookies", "cors"])
    p.add_argument("url")
    a = p.parse_args()
    try:
        status, headers = request(a.url, "https://review.invalid" if a.mode == "cors" else None)
        print(json.dumps(analyze(a.mode, status, headers), sort_keys=True))
    except (ValueError, OSError, http.client.HTTPException) as error:
        p.exit(1, f"Review failed: {type(error).__name__}\n")

if __name__ == "__main__": main()
