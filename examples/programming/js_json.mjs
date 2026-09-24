try {
  const row = JSON.parse('{"status":200,"path":"/"}');
  if (!row || typeof row !== "object" || Array.isArray(row) || !Number.isInteger(row.status)) {
    throw new Error("Invalid record shape");
  }
  console.log(JSON.stringify(row));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
