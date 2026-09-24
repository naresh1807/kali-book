import unittest
from flow_review import evaluate

class EvidenceTests(unittest.TestCase):
    def row(self, **changes):
        value=dict(name="Synthetic",source_zone="guest",destination="192.0.2.20",protocol="tcp",port=22,expected="deny",observed="reachable")
        value.update(changes)
        return value
    def test_unexpected_reachability(self):self.assertEqual("fail",evaluate(self.row()))
    def test_expected_reachability(self):self.assertEqual("pass",evaluate(self.row(expected="allow")))
    def test_verified_block(self):self.assertEqual("pass",evaluate(self.row(observed="policy_blocked")))
    def test_blocked_required_path(self):self.assertEqual("fail",evaluate(self.row(expected="allow",observed="policy_blocked")))
    def test_timeout_is_unknown(self):
        for expected in ("allow","deny"):self.assertEqual("inconclusive",evaluate(self.row(expected=expected,observed="timeout")))
    def test_closed_not_firewall_proof(self):self.assertEqual("inconclusive",evaluate(self.row(observed="closed")))
    def test_closed_required_path(self):self.assertEqual("fail",evaluate(self.row(expected="allow",observed="closed")))
    def test_invalid_port(self):
        for port in (True,0,65536,"22"):
            with self.assertRaises(ValueError):evaluate(self.row(port=port))
    def test_invalid_evidence(self):
        with self.assertRaises(ValueError):evaluate(self.row(observed="probably safe"))
    def test_scope_and_protocol(self):
        for change in ({"destination":"127.0.0.1"},{"protocol":"udp"},{"extra":"ignored"}):
            with self.assertRaises(ValueError):evaluate(self.row(**change))

if __name__ == "__main__":unittest.main()
