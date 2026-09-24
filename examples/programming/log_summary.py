import json, sys
from pathlib import Path
from collections import Counter

def summarize(path):
    with Path(path).open("rb") as stream:
        data = stream.read(1_048_577)
    if len(data) > 1_048_576:
        raise ValueError("Input exceeds 1 MiB")
    counts = Counter()
    total = 0
    for number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict) or type(row.get("status")) is not int or not 100 <= row["status"] <= 599:
            raise ValueError(f"Invalid status on line {number}")
        counts[str(row["status"])] += 1
        total += 1
    return {"records": total, "statuses": dict(sorted(counts.items()))}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 log_summary.py sample.jsonl", file=sys.stderr)
        sys.exit(2)
    try:
        print(json.dumps(summarize(sys.argv[1]), sort_keys=True))
    except (OSError, ValueError) as error:
        print(f"Cannot summarize: {error}", file=sys.stderr)
        sys.exit(1)
