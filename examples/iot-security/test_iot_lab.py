import unittest
from iot_lab import can_read, can_publish, TelemetryPolicy

class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = TelemetryPolicy()
    def send(self, seq=1, temp=22.5, device="sensor-a"):
        return self.policy.accept(device, f"lab/{device}/telemetry", {"sequence": seq, "temperature": temp})
    def test_owner(self):
        self.assertTrue(can_read("alice", "sensor-a"))
        self.assertFalse(can_read("bob", "sensor-a"))
        self.assertFalse(can_read(None, "missing"))
    def test_exact_topic(self):
        self.assertTrue(can_publish("sensor-a", "lab/sensor-a/telemetry"))
        for topic in ["lab/sensor-b/telemetry", "lab/+/telemetry", "lab/#", "lab/sensor-a/commands"]:
            self.assertFalse(can_publish("sensor-a", topic))
    def test_unknown_identity(self):
        self.assertFalse(self.send(device="unknown"))
        self.assertEqual({}, self.policy.last)
    def test_replay_and_order(self):
        self.assertTrue(self.send(2))
        self.assertFalse(self.send(2))
        self.assertFalse(self.send(1))
        self.assertTrue(self.send(3))
    def test_independent_sequences(self):
        self.assertTrue(self.send(1))
        self.assertTrue(self.send(1, device="sensor-b"))
    def test_invalid_numbers(self):
        for value in [True, "22", None, float("nan"), float("inf"), -41, 86, 10**400]:
            self.assertFalse(self.send(temp=value))
        self.assertTrue(self.send())
    def test_invalid_sequence(self):
        for value in [True, 1.0, "1", -1, 2147483648]:
            self.assertFalse(self.send(seq=value))
    def test_exact_schema(self):
        for payload in [None, [], {}, {"sequence": 1}, {"sequence": 1, "temperature": 22, "command": "open"}]:
            self.assertFalse(self.policy.accept("sensor-a", "lab/sensor-a/telemetry", payload))
    def test_invalid_does_not_advance_state(self):
        self.assertFalse(self.send(999, 100))
        self.assertTrue(self.send(1, 22))
    def test_restart_limit(self):
        self.assertTrue(self.send())
        self.policy = TelemetryPolicy()
        self.assertTrue(self.send())  # Deliberate documented limit: no durable replay state.

if __name__ == "__main__":
    unittest.main()
