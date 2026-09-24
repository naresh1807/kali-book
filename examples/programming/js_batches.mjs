const values = [1, 2, 3, 4];
const results = [];
for (let i = 0; i < values.length; i += 2) {
  const batch = values.slice(i, i + 2);
  results.push(...await Promise.all(batch.map(async x => x * 2)));
}
console.log(results);
