# API security tools: local practice

Extract the full lab ZIP. Copy examples/advanced-casebook into ~/kali-lab/advanced-casebook in Kali. Python 3.10+ is required. curl and jq are prerequisites for the shell workflow below; Burp and Postman are optional, separately installed clients. These commands use Kali Bash, not PowerShell. Credentials are public synthetic fixtures. The server has no production OAuth, JWT, GraphQL, administrator operation or rate limiter.

## Start and verify

Terminal A:
```sh
cd "$HOME/kali-lab/advanced-casebook"
python3 lab_app.py --mode fixed --port 8901
```
Terminal B:
```sh
cd "$HOME/kali-lab/advanced-casebook"
python3 exercise.py --expect fixed --case api
python3 -m unittest -v test_lab
```
Expected: all eight API checks pass. The full Python suite checks additional casebook behaviors. Stop Terminal A with Ctrl+C after use. To reproduce intentional weaknesses, restart with --mode vulnerable and run exercise.py --expect vulnerable --case api, then return to fixed mode and retest. Passing vulnerable-mode checks means the weaknesses reproduced.

## curl and jq: authenticate and compare

In Terminal B, with the fixed server running:
```sh
PENDING=$(curl --silent --show-error --max-time 5 --fail -H 'Content-Type: application/json' --data '{"user":"alice","password":"alice-lab"}' http://127.0.0.1:8901/login | jq -er '.token')
TOKEN=$(curl --silent --show-error --max-time 5 --fail -H 'Content-Type: application/json' -H "Authorization: Bearer $PENDING" --data '{"code":"123456"}' http://127.0.0.1:8901/mfa | jq -er '.token')
curl --silent --show-error --max-time 5 -i -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8901/api/invoices/1
curl --silent --show-error --max-time 5 -i -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8901/api/invoices/2
curl --silent --show-error --max-time 5 -i -X PATCH -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" --data '{"role":"admin"}' http://127.0.0.1:8901/api/profile
curl --silent --show-error --max-time 5 -i -H "Authorization: Bearer $TOKEN" 'http://127.0.0.1:8901/api/invoices?limit=11'
unset PENDING TOKEN
```
Stop and inspect any login/MFA error before continuing. Expected statuses in order after authentication: 200 (Alice own invoice), 403 (Bob invoice), 400 (role write), 400 (list bound). --max-time bounds each request; -i displays response headers; --data supplies a POST body unless another method is selected; -X PATCH selects PATCH; jq -er extracts a token and reports null/false or parsing errors. None of these commands follows redirects. Headers shown by -i are response headers, but shell variables and process arguments still contain lab credentials; use only these synthetic credentials here.

## Postman collection

Import local-api.postman_collection.json and use the desktop collection runner to execute all 14 requests sequentially against fixed mode, with one iteration. The URLs are literal loopback addresses. Test scripts keep fixture tokens in runtime variables and clear them on the final request. Do not replace them with production tokens or export a real authenticated workspace. Review the actual sharing settings of your client.

Expected: every status/body assertion passes. Vulnerable mode should cause policy assertions to fail. Login and MFA are fixture prerequisites, not a real identity provider. The collection does not run load tests, discovery or external requests.

## Burp Repeater

Scope the project to http://127.0.0.1:8901. Create or capture one fixture request, send it to Repeater and duplicate it. Compare invoice 1 versus 2 under the same synthetic Alice token; compare Bob own request separately. Keep method, headers and body identical apart from the tested variable. Record status, returned identity and body. Avoid saving bearer values in reports. Proxying localhost may require configuring the client proxy bypass settings; Repeater can send directly without proxying a browser.

## ZAP and GraphiQL

ZAP can provide a proxy/history and passive observations for manually sent fixture requests. Passive findings do not establish ownership policy, and active scanning is a separate operation; no scan is required for this exercise. GraphiQL requires a separate local GraphQL server and known schema. This REST fixture cannot demonstrate GraphQL, JWT, OAuth or rate limiting. Use the chapter worksheets to define those tests before selecting another lab.

## Evidence worksheet

Account | method/path | changed field | expected identity/status | observed | repair | retest. Label credentials without recording values. Preserve successful authorized operations as negative controls against overblocking.
