const counts = new Map();
for (const status of [200, 404, 200]) {
  counts.set(status, (counts.get(status) ?? 0) + 1);
}
console.log([...counts.entries()]);
