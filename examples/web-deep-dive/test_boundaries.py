import unittest
from boundary_lab import database, unsafe_lookup, bound_lookup, html_text, unsafe_fulfill, transition, demonstrate

class QueryTests(unittest.TestCase):
    def setUp(self): self.db = database()
    def tearDown(self): self.db.close()
    def test_owner_baseline(self):
        self.assertEqual([(1, "alice", 100)], bound_lookup(self.db, "alice"))
    def test_other_owner(self):
        self.assertEqual([(2, "bob", 200)], bound_lookup(self.db, "bob"))
    def test_missing_owner(self):
        self.assertEqual([], bound_lookup(self.db, "nobody"))
    def test_injection_negative_control(self):
        value = "alice' OR 1=1 -- "
        self.assertEqual(3, len(unsafe_lookup(self.db, value)))
        self.assertEqual([], bound_lookup(self.db, value))
    def test_legitimate_apostrophe(self):
        self.assertEqual([(3, "o'reilly", 50)], bound_lookup(self.db, "o'reilly"))
    def test_query_does_not_change_rows(self):
        bound_lookup(self.db, "unmatched'")
        self.assertEqual(3, self.db.execute("SELECT count(*) FROM invoices").fetchone()[0])

class RenderingTests(unittest.TestCase):
    def test_markup_text(self):
        self.assertEqual('<p>&lt;em&gt;marker&lt;/em&gt;</p>', html_text('<em>marker</em>'))
    def test_ampersand_and_quotes(self):
        self.assertEqual('<p>A &amp; &quot;B&quot;</p>', html_text('A & "B"'))
    def test_normal_text(self):
        self.assertEqual('<p>Hello</p>', html_text('Hello'))

class WorkflowTests(unittest.TestCase):
    def test_valid_payment_then_fulfillment(self):
        self.assertEqual('fulfilled', transition(transition('draft', 'pay'), 'fulfill'))
    def test_skip_payment_negative_control(self):
        self.assertEqual('fulfilled', unsafe_fulfill('draft'))
        with self.assertRaises(ValueError): transition('draft', 'fulfill')
    def test_repeat_fulfillment(self):
        with self.assertRaises(ValueError): transition('fulfilled', 'fulfill')
    def test_cancelled_order_cannot_pay(self):
        with self.assertRaises(ValueError): transition(transition('draft', 'cancel'), 'pay')
    def test_all_demonstrations(self):
        self.assertTrue(all(demonstrate().values()))

if __name__ == '__main__': unittest.main()
