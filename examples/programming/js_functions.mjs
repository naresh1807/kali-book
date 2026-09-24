function validPort(value) {
  return Number.isInteger(value) && value >= 1 && value <= 65535;
}
for (const value of [443, 0, "443", true]) console.log(value, validPort(value));
