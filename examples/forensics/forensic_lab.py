"""Offline integrity and timezone demonstration; reads only supplied fixture files."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def verify(root, manifest):
    root = Path(root).resolve()
    if not isinstance(manifest, dict) or not manifest:
        raise ValueError("Expected nonempty filename-to-SHA256 manifest")
    result = {}
    for name, digest in manifest.items():
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_-]+\.[A-Za-z0-9]+", name):
            raise ValueError("Fixture manifest requires simple filenames")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("Invalid SHA256")
        path = root / name
        if path.is_symlink() or path.resolve().parent != root:
            raise ValueError("Evidence path must stay in the fixture directory")
        result[name] = "missing" if not path.is_file() else ("match" if hashlib.sha256(path.read_bytes()).hexdigest() == digest else "mismatch")
    return result


def timeline(text):
    records = []
    seen = set()
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip(): continue
        row = json.loads(line)
        required = {"id", "source", "timestamp", "event"}
        if not isinstance(row, dict) or set(row) != required or not all(isinstance(v, str) and v for v in row.values()):
            raise ValueError("Malformed event record")
        if row["id"] in seen: raise ValueError("Duplicate event id")
        seen.add(row["id"])
        stamp = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("Explicit timezone offset required")
        utc = stamp.astimezone(timezone.utc)
        records.append((utc, {**row, "source_line": line_no, "utc": utc.isoformat().replace("+00:00", "Z")}))
    # Stable sorting preserves source order for tied timestamps without claiming causal order.
    records.sort(key=lambda x: x[0])
    return [row for _, row in records]


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    integrity = verify(root, manifest)
    if not all(x == "match" for x in integrity.values()):
        print(json.dumps({"integrity": integrity, "analysis": "stopped: fixture differs from baseline"}, indent=2))
        raise SystemExit(1)
    rows = timeline((root / "events.jsonl").read_text(encoding="utf-8"))
    print(json.dumps({"synthetic": True, "integrity": integrity, "timeline": rows, "limits": "Hashes compare against a supplied baseline; they do not authenticate origin. Equal times do not establish event order."}, indent=2))
