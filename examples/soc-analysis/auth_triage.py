"""Offline synthetic authentication triage; no network or persistent database."""
import sqlite3
EVENTS = [
 ('2026-01-01T09:54:59Z','trainee-a','failure'),
 ('2026-01-01T09:55:00Z','trainee-a','failure'),
 ('2026-01-01T09:57:00Z','trainee-a','failure'),
 ('2026-01-01T10:00:00Z','trainee-a','failure'),
 ('2026-01-01T09:59:00Z','trainee-a','success'),
 ('2026-01-01T09:58:00Z','trainee-b','failure'),
 ('2026-01-01T10:00:01Z','trainee-a','failure'),
]
QUERY = """SELECT account, count(*) AS failures FROM events
WHERE outcome = 'failure' AND ts >= ? AND ts <= ?
GROUP BY account HAVING count(*) >= ? ORDER BY account"""
def triage(events, start='2026-01-01T09:55:00Z', end='2026-01-01T10:00:00Z', threshold=3):
    if start > end or not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 1:
        raise ValueError('Use an ordered window and a positive integer threshold')
    db = sqlite3.connect(':memory:')
    try:
        db.execute('CREATE TABLE events (ts TEXT, account TEXT, outcome TEXT)')
        db.executemany('INSERT INTO events VALUES (?,?,?)', events)
        return db.execute(QUERY, (start, end, threshold)).fetchall()
    finally:
        db.close()
if __name__ == '__main__':
    print('Synthetic leads only; investigate context before declaring an incident.')
    for account, count in triage(EVENTS):
        print(account, count)
