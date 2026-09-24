from collections import Counter
rows = [{"status": 200}, {"status": 404}, {"status": 200}]
counts = Counter(row["status"] for row in rows)
for status, count in sorted(counts.items()):
    print(status, count)
