import http.client, json, sys

def inspect(port):
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
    try:
        connection.request("HEAD", "/")
        response = connection.getresponse()
        names = ["content-type", "content-security-policy", "x-content-type-options"]
        return {"status": response.status, "headers": {name: response.getheader(name) for name in names}}
    finally:
        connection.close()

if __name__ == "__main__":
    try:
        if len(sys.argv) > 2:
            raise ValueError("Usage: python3 local_headers.py [port]")
        port = int(sys.argv[1]) if len(sys.argv) == 2 else 8877
        if not 1 <= port <= 65535:
            raise ValueError("Port must be 1..65535")
        print(json.dumps(inspect(port), sort_keys=True))
    except (ValueError, OSError, http.client.HTTPException) as error:
        print(f"Cannot inspect: {error}", file=sys.stderr)
        sys.exit(1)
