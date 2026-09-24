async function readSyntheticResult() {
  return {status: 200};
}
try {
  const result = await readSyntheticResult();
  console.log(result.status);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
