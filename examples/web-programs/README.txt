WEB APPLICATION TESTING PROGRAMS

Copy this folder into ~/kali-lab/web-programs in Kali. A host drive is not automatically mounted inside the VM.
Python 3.10+ and a supported Node release are required. No third-party packages are used.

Terminal A:
python3 fixture_server.py --port 8891

Terminal B (from this folder):
python3 web_review.py headers http://127.0.0.1:8891/strong
node web_review.mjs cookies http://127.0.0.1:8891/strong
python3 web_review.py cors http://127.0.0.1:8891/cors
node web_review.mjs headers http://127.0.0.1:8891/redirect
python3 response_diff.py baseline.json denied.json
node response_diff.mjs baseline.json ambiguous.json

Browser exercise:
Open http://127.0.0.1:8891/ in a lab browser and read browser_inventory.js before running it in Developer Tools Console. It inspects links/forms without following links or submitting forms.

Each web_review invocation makes one GET, does not follow redirects and omits bodies/cookie values from output. It accepts explicit HTTP(S) URLs: use only authorized targets. TLS verification remains enabled. Python uses per-operation timeouts; Node uses a request deadline. Large bodies fail at 256 KiB. No authentication or CORS preflight is attempted.

response_diff inputs are custom JSON with status (integer 100..599) and body (string). Files are limited to 1 MiB. Fixture data is fictional. Reports are observations, not vulnerability verdicts. Ctrl+C stops the fixture server.
