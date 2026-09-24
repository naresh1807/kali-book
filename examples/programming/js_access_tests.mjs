import test from "node:test";
import assert from "node:assert/strict";
const canRead = (user, record) => user.tenant === record.tenant && user.id === record.owner;
test("owner may read", () => assert.equal(canRead({id:1,tenant:"A"}, {owner:1,tenant:"A"}), true));
test("other tenant denied", () => assert.equal(canRead({id:1,tenant:"B"}, {owner:1,tenant:"A"}), false));
test("other user denied", () => assert.equal(canRead({id:2,tenant:"A"}, {owner:1,tenant:"A"}), false));
