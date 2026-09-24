import {createHash} from "node:crypto";
const data = Buffer.from("lab evidence", "utf8");
console.log(data.toString("utf8"));
console.log(createHash("sha256").update(data).digest("hex"));
