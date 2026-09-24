"""Offline teaching policy. No network, broker, cryptography or device control."""
import json
import math

OWNERS = {"sensor-a": "alice", "sensor-b": "bob"}

def can_read(user, device):
    return device in OWNERS and OWNERS[device] == user

def can_publish(identity, topic):
    # identity must come from a separate, trusted authentication layer.
    return identity in OWNERS and topic == f"lab/{identity}/telemetry"

class TelemetryPolicy:
    def __init__(self):
        self.last = {}

    def accept(self, identity, topic, payload):
        if not can_publish(identity, topic):
            return False
        if not isinstance(payload, dict) or set(payload) != {"sequence", "temperature"}:
            return False
        sequence, temperature = payload["sequence"], payload["temperature"]
        if type(sequence) is not int or not 0 <= sequence <= 2147483647:
            return False
        if type(temperature) not in (int, float) or not -40 <= temperature <= 85 or not math.isfinite(temperature):
            return False
        if sequence <= self.last.get(identity, -1):
            return False
        self.last[identity] = sequence
        return True

if __name__ == "__main__":
    policy = TelemetryPolicy()
    message = {"sequence": 1, "temperature": 22.5}
    results = {
        "owner_read_allowed": can_read("alice", "sensor-a"),
        "other_owner_denied": not can_read("bob", "sensor-a"),
        "own_telemetry_allowed": policy.accept("sensor-a", "lab/sensor-a/telemetry", message),
        "replay_denied": not policy.accept("sensor-a", "lab/sensor-a/telemetry", message),
        "other_topic_denied": not policy.accept("sensor-a", "lab/sensor-b/telemetry", message),
    }
    print(json.dumps(results, indent=2))
    raise SystemExit(0 if all(results.values()) else 1)
