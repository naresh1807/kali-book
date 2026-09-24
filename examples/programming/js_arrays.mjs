const rows = [{status:200}, {status:404}, {status:403}];
console.log(rows.filter(row => row.status >= 400).map(row => row.status));
