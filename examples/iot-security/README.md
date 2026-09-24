# Offline IoT authorization and replay lab

This Python 3 standard-library simulator opens no sockets and controls no hardware. It is not an MQTT implementation. The caller identity is assumed to come from a trusted authentication layer; changing the identity argument demonstrates why authentication is necessary, not an authentication bypass in a real product.

From this extracted directory, run:

```sh
python3 iot_lab.py
python3 -m unittest -v
```

On Windows, use `python` if that is your installed interpreter command. Expect five demonstration results set to true and ten passing tests. No packages or device credentials are needed.

1. Explain why Alice can read sensor-a and Bob cannot. Compare exact topic authorization with wildcard requests.
2. Follow a valid reading, a replay, and a malformed reading. Verify that malformed input does not consume a sequence number.
3. In a separate copy, make can_publish return True. Run the tests and record the failures. Restore the function and confirm they pass. This negative control checks that the tests detect an authorization regression.
4. Write a report with expected behavior, observed behavior, minimal evidence, repair and retest result. Use synthetic names only.

Limits: identities and owners are hardcoded; replay state is in memory and resets on restart; no locks support concurrent consumers. Temperature bounds are a fictional sensor policy. This does not implement certificate verification, cryptographic message authentication, MQTT session behavior, firmware signatures, durable counters or a production broker. Real designs need an authenticated epoch/reset policy, durable or otherwise appropriate freshness protection and concurrency handling. The restart test deliberately documents a limitation rather than proving durable protection.
