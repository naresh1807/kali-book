# Advanced web-security casebook lab

This is original, synthetic training software. It binds only to IPv4 loopback. Fixed mode is the default. The deliberately vulnerable mode changes object authorization, writable profile fields and pending-session/token-rotation behavior. Other protections, including webhook validation and atomic redemption, remain in both modes.

Requires Python 3.10+ with standard libraries. Browser-policy tests also use Node.js. No dependency installation or real account is needed.

Copy this folder into `~/kali-lab/advanced-casebook` inside Kali; A host drive is not automatically mounted there.

## First run

Terminal A:

```sh
cd "$HOME/kali-lab/advanced-casebook"
python3 lab_app.py --mode vulnerable --port 8901
```

Terminal B:

```sh
cd "$HOME/kali-lab/advanced-casebook"
python3 exercise.py --expect vulnerable --case api
```

Stop Terminal A with Ctrl+C. Restart with `--mode fixed`, then run the same exercise with `--expect fixed`. The reports compare observed behavior to the selected mode. A passing vulnerable-mode exercise means the weakness reproduced, not that the app is secure.

## Full checks

```sh
python3 -m unittest -v test_lab
node browser_tests.cjs
python3 race_demo.py
python3 auth_binding.py
```

The test suite starts temporary loopback servers on free ports and shuts them down. The browser tests check message-policy logic in Node; browser CSP behavior must be inspected manually in the browser exercise.

## Exercise groups

`exercise.py --case api`, `--case auth`, `--case logic`, `--case webhook`, or `--case all`. Add `--port` if you changed the default. Restart the app before repeating `logic` or `all`, because successful redemption consumes the synthetic coupon. Restarting resets all in-memory state.

Alice: `alice` / `alice-lab`; Bob: `bob` / `bob-lab`. MFA code: `123456`. All are public training fixtures. POST `/login` obtains a pending token; POST `/mfa` exchanges it for a complete token in fixed mode. Use `Authorization: Bearer TOKEN`. The exercise client handles these steps without printing tokens.

Routes: GET `/api/invoices/1`, `/api/invoices/2`, `/api/invoices?limit=1`, `/api/v1/invoices`, `/api/profile`; PATCH `/api/profile`; POST `/redeem`, `/logout`, `/webhook`. Requests use synthetic JSON. `/` serves the browser trust exercise, not a login UI.

The webhook secret is a public fixture in lab_app.py, not a deployable secret. Request bodies are limited to 4096 bytes. This toy server is not hardened production software: it has no real password storage, real MFA, OAuth provider, JWT verifier, GraphQL engine, persistent database, rate limiter or production session lifecycle. The book explains those separate designs and their test requirements.

## Capstone

Use the accompanying threat-model, code-review and report worksheets. Preserve request context and expected policy; do not put real secrets into evidence. Do not expose this lab through a bridge, public bind address or port forwarding.
