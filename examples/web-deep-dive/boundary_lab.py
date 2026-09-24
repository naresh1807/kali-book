"""Synthetic, in-memory boundary demonstrations. No sockets or external database."""
import html
import json
import sqlite3


def database():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE invoices (id INTEGER, owner TEXT, amount INTEGER)")
    db.executemany("INSERT INTO invoices VALUES (?, ?, ?)", [(1, "alice", 100), (2, "bob", 200), (3, "o'reilly", 50)])
    return db


def unsafe_lookup(db, owner):
    # Deliberately vulnerable teaching code, used only on the in-memory fixture.
    sql = "SELECT id, owner, amount FROM invoices WHERE owner = '" + owner + "' ORDER BY id"
    return db.execute(sql).fetchall()


def bound_lookup(db, owner):
    return db.execute("SELECT id, owner, amount FROM invoices WHERE owner = ? ORDER BY id", (owner,)).fetchall()


def html_text(value):
    # HTML text encoding only, not JavaScript, CSS or URL encoding.
    return "<p>" + html.escape(value, quote=True) + "</p>"


def unsafe_fulfill(state):
    return "fulfilled"


def transition(state, action):
    rules = {("draft", "pay"): "paid", ("paid", "fulfill"): "fulfilled", ("draft", "cancel"): "cancelled"}
    try:
        return rules[(state, action)]
    except KeyError:
        raise ValueError("Transition not allowed") from None


def demonstrate():
    db = database()
    try:
        teaching_input = "alice' OR 1=1 -- "
        try:
            transition("draft", "fulfill")
            denied = False
        except ValueError:
            denied = True
        results = {
            "ordinary_lookup_returns_one": len(bound_lookup(db, "alice")) == 1,
            "unsafe_query_expands_to_three_rows": len(unsafe_lookup(db, teaching_input)) == 3,
            "bound_query_treats_same_input_as_data": bound_lookup(db, teaching_input) == [],
            "apostrophe_in_legitimate_name_works": len(bound_lookup(db, "o'reilly")) == 1,
            "markup_is_encoded_as_text": html_text("<em>marker</em>") == "<p>&lt;em&gt;marker&lt;/em&gt;</p>",
            "unsafe_workflow_skips_payment": unsafe_fulfill("draft") == "fulfilled",
            "fixed_workflow_blocks_skip": denied,
            "valid_workflow_still_works": transition(transition("draft", "pay"), "fulfill") == "fulfilled",
        }
        return results
    finally:
        db.close()

if __name__ == "__main__":
    results = demonstrate()
    print(json.dumps(results, indent=2))
    raise SystemExit(0 if all(results.values()) else 1)
