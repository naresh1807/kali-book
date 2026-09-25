# Red Team workbook

## 1. Engagement planning template

Business objective and decision to inform:
Authorized systems and identities:
Excluded assets and actions:
Permitted timeframe and source locations:
Exercise owner and emergency contact:
Stop conditions and escalation procedure:
Expected operational effects:
Synthetic data and evidence retention:
Defender visibility and coordination:
Cleanup owner and acceptance criteria:

Use the loopback exercise below as the first plan. This workbook does not authorize testing unrelated devices or external services.

## 2. Local service observation: Python, Nmap and curl

Prerequisites: Python 3, Nmap and curl installed separately. Extract this red-team folder and run the server only from it so unrelated files are not exposed. The included marker is synthetic. If port 8765 is already occupied, stop and identify the conflict rather than testing an unknown service.

Terminal A, from the extracted red-team folder:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

On Windows, use python if python3 is unavailable. The server binds only to loopback. Keep it running for the next two commands in Terminal B:

```sh
nmap -sT -p 8765 --reason 127.0.0.1
curl --max-time 5 --fail http://127.0.0.1:8765/marker.txt
```

-sT uses a TCP connect scan, -p selects one port and --reason explains the state observation. Expected while the server runs: port 8765 is open. That proves local reachability, not a vulnerability. curl retrieves the harmless marker; --max-time bounds the request and --fail reports HTTP errors. Windows PowerShell users should call curl.exe to avoid a legacy alias.

Observe the request in the server console. Record timestamps, source, requested path and response status. Press Ctrl+C in Terminal A to stop the server. Confirm the process stopped and a repeat request no longer returns the marker. A snapshot is not needed to remove this temporary process, but retain your evidence notes.

## 3. Tool selection and usage

Nmap: answer a bounded reachability question first; interpret results from the tested location. Use the loopback command above before considering broader authorized inventories.

Burp Suite: with an existing lab installation, use its integrated browser to visit the loopback marker URL, then inspect Proxy HTTP history. Inspect method, path, status and body. If loopback bypasses your proxy configuration, verify the browser proxy settings rather than assuming no request happened. Do not enable active scanning for this observation exercise.

Wireshark/TShark: inspect an authorized saved capture to correlate network observations; the SOC tools workbook explains filters and expected limitations. No capture is supplied in this folder.

ATT&CK Navigator: use a local or approved instance to create a layer for the few behaviors in the plan. Document evidence and scope in notes; coloring a technique does not establish tested coverage.

BloodHound: study identity relationships using an approved lab dataset. Record each path prerequisite and validate permissions with the system owner. No directory collector is run by this book, and a graph path alone is not proof of exploitability.

Atomic Red Team: inspect test definitions and their prerequisite and cleanup sections before choosing a lab test. Review the exact commands and dependencies; do not bulk-execute a technique collection. Verify restoration independently after any separately approved test.

MITRE Caldera: review an operation plan and its abilities in a disposable lab before deployment. Identify every action, credential, target, external connection and cleanup task. This workbook does not install agents or create operations.

These tools serve different questions. Start with the local observation exercise, then progress to emulation only when the lab and detection plan are ready.

## 4. Operator and defender evidence matrix

For each step record: objective, test action, expected sensor, observed event, alert or case, analyst decision, limitation, cleanup and owner.

Example: retrieving marker.txt creates an HTTP request observable in the local server log. It does not establish that an enterprise proxy, EDR or SIEM collected the event. Mark those stages untested unless you actually configured and verified them.

Compare a positive observation with a negative control, such as requesting a nonexistent harmless path. Explain the difference between a 404 response and a blocked connection. Do not label either as an exploit.

## 5. References and progression

[MITRE adversary emulation plans](https://attack.mitre.org/resources/adversary-emulation-plans/)
[MITRE CTID micro emulation](https://ctid.mitre.org/projects/micro-emulation-plans/)
[Atomic Red Team getting started](https://github.com/redcanaryco/atomic-red-team/wiki/Getting-started)
[MITRE Caldera](https://github.com/mitre/caldera)
[Nmap reference](https://nmap.org/book/man.html)
[Python HTTP server](https://docs.python.org/3/library/http.server.html)
[ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator)
[BloodHound documentation](https://bloodhound.specterops.io/)

Lessons 01-07 cover foundations; 08-14 examine access boundaries and emulation planning; 15-20 connect evidence, defender validation and reporting. Tools are documented for manual practice, not installed or executed by the website.


## 6. Tool setup and choosing the right question

Start with the loopback server in workbook section 2. Run it from this extracted red-team folder only. Commands below assume that server is listening on 127.0.0.1:8765. Tools are installed separately; use the official distribution or your supported package manager, record versions and inspect installed help. Do not install similarly named packages without verifying the publisher.

Learning sequence: curl checks a single request; Nmap checks a port; Burp or ZAP explains HTTP; ffuf compares two fixture paths; Metasploit illustrates module configuration. Identity and emulation tools come later, in a separate disposable lab.

Command blocks are manual examples. No tool is launched by the book. Read prerequisites and expected effects before a command. Stop on a failed prerequisite rather than substituting a random reachable service. The local server is a teaching fixture, not a production deployment.

Record for each tool: version, target, input, command, timestamp, observation, uncertainty and cleanup. A successful command is not automatically a security finding.


## 7. curl: requests, headers and negative controls

Use: inspect one HTTP transaction before automating a larger test. Setup: curl installed and the loopback server running. In Windows PowerShell, use curl.exe to avoid older aliases.

```sh
curl --max-time 5 -i http://127.0.0.1:8765/marker.txt
curl --max-time 5 -I http://127.0.0.1:8765/marker.txt
curl --max-time 5 -i http://127.0.0.1:8765/missing-training-file.txt
```

-i includes response headers with the body; -I requests headers using HEAD; --max-time bounds the operation. Expect 200 and the marker for the first request, headers without the marker body for the second, and 404 for the nonexistent path.

Interpretation: distinguish connection failure, HTTP error and unexpected content. A 200 status alone does not prove authorized access or a vulnerability. These requests write server access logs but do not change fixture files.

Practice: compare Content-Length with the downloaded bytes. Keep redirects disabled until you verify their destinations are within scope. Cleanup: stop the shared server after completing all exercises.

Reference: https://curl.se/docs/manpage.html


## 8. Nmap: reachability and service identification

Use: answer which approved service is reachable from your test location. Setup: Nmap installed; start with one loopback port.

```sh
nmap -sT -p 8765 --reason 127.0.0.1
nmap -sT -sV --version-light -p 8765 127.0.0.1
```

-sT performs a TCP connection test; -p constrains the port; --reason explains the observed state. -sV adds application probes and --version-light uses a lighter version-detection intensity. It still sends additional traffic.

Expect an open port while the fixture runs. Identification text depends on Nmap and server versions; treat a reported product or version as a hypothesis. Confirm with headers and the known process. This does not establish a CVE or remote exploitability.

Practice: compare with a stopped fixture. An unexpected open result means another service may be using the port: investigate before continuing. Cleanup: no persistent service is installed by the scan; retain results and stop the fixture when finished.

Reference: https://nmap.org/book/man-version-detection.html


## 9. Burp Suite: Proxy history and Repeater

Use: inspect and carefully vary HTTP requests. Setup: an installed Burp lab instance and its integrated browser. Scope the target to the loopback fixture; keep automated scanning out of this introductory exercise.

Step 1: open the browser through Burp and visit http://127.0.0.1:8765/marker.txt. If interception pauses navigation, forward the request or turn interception off while retaining history.

Step 2: find the request in Proxy HTTP history. Inspect the method, path, host header, status and response body. If no request appears, check the selected browser and loopback proxy-bypass configuration.

Step 3: send the request to Repeater. Send the unchanged request first as a baseline. Change only the path to /missing-training-file.txt and send again. Expect 200 then 404. Restore the original path and confirm the original response.

Interpretation: one-variable comparisons support a hypothesis. In an owned app with synthetic accounts, this method can examine authorization, but the static fixture has no login or protected records. Do not claim it tests account boundaries.

Cleanup: close the lab browser, remove temporary proxy settings if you configured them manually and protect any saved project containing real session data.

Reference: https://portswigger.net/burp/documentation/desktop/tools/repeater


## 10. OWASP ZAP: manual exploration and passive review

Use: proxy HTTP and review potential issues in observed traffic. Setup: installed ZAP with a browser launched through its manual exploration workflow. Use Safe mode for this exercise and the local fixture URL.

Step 1: choose manual exploration, not the Automated Scan action. Browse marker.txt and the nonexistent fixture path.

Step 2: inspect Sites/History, select each transaction and compare request and response. Passive rules analyze the observed messages; browsing still sends traffic.

Step 3: review any alerts individually. Record the evidence, the rule explanation and whether it is relevant to a static training server. Missing headers on this fixture do not by themselves establish a severe application vulnerability.

Expected: the visited URLs and their responses appear. Alert count depends on enabled add-ons and rules, so there is no fixed expected count. The Automated Scan workflow can crawl and actively test; it is a separate action requiring a suitable lab and plan.

Cleanup: close the test browser, save only needed evidence and restore manually changed proxy settings.

Reference: https://www.zaproxy.org/docs/desktop/start/


## 11. ffuf: bounded path comparison

Use: compare responses for a small explicit input list. Setup: ffuf installed, paths.txt from this download and the loopback server running. The list contains only marker.txt and a nonexistent path.

```sh
ffuf -w paths.txt -u http://127.0.0.1:8765/FUZZ -t 1 -rate 1 -maxtime 10 -mc all
```

-w supplies inputs; FUZZ marks substitution; -t 1 limits concurrency; -rate 1 limits requests per second; -maxtime bounds total runtime; -mc all displays all response statuses. Expect one 200 and one 404 for this fixture.

Interpretation: response size and status help compare behavior, but a soft-404 can return 200 for missing content on other applications. Establish a negative control before filtering away responses. This example deliberately avoids recursion and large wordlists.

Practice: inspect both paths with curl and correlate the two requests with server logs. Do not expand the wordlist until the exercise objective calls for it. Cleanup: no fixture files change; stop the shared server when finished.

Reference: https://github.com/ffuf/ffuf


## 12. ProjectDiscovery httpx: HTTP observations

Use: summarize HTTP endpoints after scope validation. Setup: the ProjectDiscovery httpx binary, which differs from the Python HTTPX library. Check its installed help first.

```sh
httpx -h
httpx -u http://127.0.0.1:8765/marker.txt -sc -cl -server -rl 1 -threads 1
```

-u selects the fixture URL; -sc shows status; -cl shows content length; -server shows server-header information; -rl and -threads bound rate and concurrency. Exact fields and output formatting depend on the installed version.

Expected: an HTTP observation for the local URL, normally status 200. Server headers are self-reported evidence and can be changed or misleading. If the command has unrelated options, confirm you installed the intended binary.

Practice: compare its output with curl. Keep scope explicit before using endpoint lists or redirect-following features. Cleanup: retain only required observations and stop the fixture after the shared exercises.

Reference: https://github.com/projectdiscovery/httpx


## 13. Metasploit: understand an auxiliary module

Use: learn module selection, options and evidence without deploying an exploit. Setup: Metasploit Framework installed in your lab and the same local HTTP fixture running. This module sends HTTP probes; it does not install a payload.

Start msfconsole, then enter:

```text
use auxiliary/scanner/http/http_version
info
show options
set RHOSTS 127.0.0.1
set RPORT 8765
set SSL false
set THREADS 1
show options
run
back
exit
```

use selects the module; info explains purpose; show options exposes current settings; set supplies bounded inputs. Verify the target and port before run. Expect a server-identification observation depending on response and module version.

Interpretation: the framework includes many different module classes with different effects. A banner check does not establish vulnerability, and a module name or rank does not guarantee suitability. Read module documentation and effects before any different module.

Practice: compare the observed banner with curl headers and the known Python server. Cleanup: exit the console and stop the fixture; no session or listener is created by this exercise.

Reference: https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/auxiliary/scanner/http/http_version.md


## 14. Wireshark and TShark: verify what happened

Use: corroborate tool output with packet evidence. Setup: an authorized saved lab.pcap and TShark installed. No capture is included; select one from your own controlled exercise.

```sh
tshark -r lab.pcap -Y "http.request" -T fields -e frame.number -e http.request.method -e http.request.uri
```

-r reads saved packets; -Y applies a display filter; -T fields chooses field output. Expect requests only when the capture contains traffic that the dissector recognizes as HTTP. If the nonstandard port is not decoded, use Wireshark Decode As for the known lab TCP stream. TLS traffic usually does not expose plaintext HTTP fields.

Practice: match a tool request to a packet timestamp and server log. Explain capture location, time zone and missing evidence. Loopback traffic requires loopback capture support when collecting it; do not expect it on every physical interface.

Cleanup: stop any separately started capture and secure evidence files; packet captures can contain credentials when real traffic is present.

Reference: https://www.wireshark.org/docs/man-pages/tshark


## 15. BloodHound: identity paths and prerequisites

Use: analyze identity relationships and possible paths to sensitive permissions. Setup: an approved local BloodHound lab and a compatible lab dataset. Collection is a separate operation with scope, permissions and data-retention implications; this tutorial does not run a collector.

Step 1: import your approved dataset according to the installed edition. Check its collection time, domain and completeness before interpreting the graph.

Step 2: locate a synthetic test user and an intended sensitive object. Inspect a candidate path one edge at a time. Read the relationship explanation and identify which principal needs which right.

Step 3: record each prerequisite, configuration dependency and uncertainty. Validate rights with the lab owner or source configuration. A shortest path is a hypothesis, not proof that every transition can be executed.

Step 4: propose removing one unnecessary permission and compare a refreshed lab dataset after remediation. Verify legitimate access still works.

Expected: interpretable relationships only when data supports them; missing nodes can reflect collection limits. Cleanup: restrict access to exported identity data and delete it according to the agreed retention policy.

Reference: https://bloodhound.specterops.io/


## 16. Atomic Red Team: inspect before selecting a test

Use: organize small behavior tests and expected defender observations. Setup: an existing disposable lab with reviewed Atomic definitions and the Invoke-AtomicRedTeam module already imported. Start with details, not bulk execution.

```powershell
Invoke-AtomicTest T1082 -ShowDetails
```

This requests details for system-information-discovery test definitions in the installed library. Read each test name, supported platform, executor, input arguments, dependencies, commands and cleanup. Test definitions can change; choose by reviewed identity rather than assuming a numeric position remains stable.

Workflow: select one test suitable for the lab, record its expected telemetry and changes, review prerequisite commands, then follow the installed documentation for that specific test. Prerequisite checks may run commands; fetching prerequisites may download software. Do not treat either as a passive text preview.

Expected at this stage: displayed definitions, not proof that behavior was executed or detected. After any separately planned execution, verify telemetry and baseline restoration; cleanup commands can be incomplete or fail.

Practice: produce a test card containing action, prerequisites, evidence source, stop condition and cleanup verification. No tests or dependencies are executed by this handbook.

Reference: https://github.com/redcanaryco/atomic-red-team/wiki/Getting-started


## 17. MITRE Caldera: review an emulation operation

Use: coordinate defined adversary-emulation actions in a controlled environment. Setup: an owned disposable lab deployment of a supported, patched version. Do not expose a training management interface publicly. This walkthrough reviews a plan; it does not deploy an agent.

Step 1: read the installed version terminology: an ability describes an action; an adversary profile groups actions; an operation applies a plan using available agents and facts. Planners determine action selection and progression.

Step 2: inspect the proposed profile. Review each command, platform, privilege requirement, payload/dependency, expected fact output and cleanup. Identify external connections and state changes explicitly.

Step 3: restrict any eventual operation to an approved lab group and establish a pause/stop process. Confirm telemetry collection before execution. Do not infer that a default planner executes only the single action you had in mind.

Step 4: for a separately authorized run, reconcile executed actions and outputs with defender evidence and verify introduced artifacts and credentials are removed. A completed operation status does not prove successful detection or cleanup.

Practice: review one fictional three-step plan on paper and explain why a missing prerequisite should prevent progression.

Reference: https://github.com/mitre/caldera
Reference: https://caldera.readthedocs.io/


## 18. ATT&CK Navigator: map tested behavior

Use: communicate what was actually exercised and observed. Setup: a trusted Navigator instance or local deployment with an appropriate ATT&CK domain/version.

Create a new layer and select only behaviors supported by the engagement plan. Add notes for test date, environment, prerequisites, data source, analytic and outcome. Use a documented color legend, such as planned, observed and validated, rather than unexplained colors.

Export the layer JSON and keep it with the report. Reopen it to verify the notes and legend survive. A colored technique means only what the evidence and legend define; it is not a universal coverage score.

Practice: distinguish planned from executed steps and collection from successful SOC response. Record untested variants and avoid counting every sub-technique when only one behavior was exercised.

Cleanup: remove sensitive system identifiers from any public layer and retain internal evidence references separately.

Reference: https://github.com/mitre-attack/attack-navigator


## 19. Evidence and cleanup: turn tool output into a finding

Use: preserve repeatable observations without overstating them. Setup: use the engagement template, local fixture logs and a new report document. No specialized reporting platform is required.

Record the exact question and baseline, then the tool version, command or UI action, target, timestamp and result. Attach the smallest evidence needed. Describe alternative explanations and limitations, such as a banner being self-reported or a graph path being unvalidated.

For the loopback exercise, report normal local reachability and the known marker response. Do not invent a vulnerability to make the exercise look successful. Compare the curl, Nmap and server observations and explain their different claims.

Cleanup: stop the Python server with Ctrl+C, exit consoles, restore manual proxy settings and confirm no test process remains. Remove temporary accounts, agents or data only if you actually created them under a separate plan. Record anything that needs an owner follow-up.

Practice: write a one-paragraph technical finding and a one-paragraph executive explanation. Include a retest criterion and a valid-use check for any proposed remediation.

Validation note: product commands are manual exercises and have not been executed against those tools here. The website checks navigation and packaged fixtures; it does not install tools or run an engagement.


## 20. Worked example: Baseline, negative control and restored baseline

Question: can the tool reliably distinguish a known file from a missing file? Start the section 2 loopback server. Run the following in a second terminal; use curl.exe in Windows PowerShell.

```sh
curl --max-time 5 -sS -o baseline.txt -w "%{http_code}\n" http://127.0.0.1:8765/marker.txt
curl --max-time 5 -sS -o negative.txt -w "%{http_code}\n" http://127.0.0.1:8765/missing-training-file.txt
curl --max-time 5 -sS -o restored.txt -w "%{http_code}\n" http://127.0.0.1:8765/marker.txt
```

Expected: 200, 404, 200. -o writes response bodies to new files; choose filenames that do not contain existing work. -w prints the response status. -sS hides progress while retaining errors. Compare baseline.txt and restored.txt: the bodies should match if the fixture did not change.

Interpretation: a repeatable baseline makes the changed path a more credible explanation of the differing response. This is normal server behavior, not a vulnerability. A timeout or connection error is not equivalent to 404. Cleanup: retain only required evidence and stop the fixture after all exercises.


## 21. Worked example: HEAD versus GET in curl and Burp

Question: does the request method change what the server sends? Use the same marker path for both requests.

```sh
curl --max-time 5 -I http://127.0.0.1:8765/marker.txt
curl --max-time 5 -i http://127.0.0.1:8765/marker.txt
```

Expected: HEAD returns metadata without the marker body; GET returns metadata and the marker. Content-Length can describe the GET body even when HEAD sends no body. Do not interpret that as data unexpectedly returned by HEAD.

In Burp Repeater, send a baseline GET, change only the method to HEAD, send again, then restore GET. Record status, headers and actual body separately. If an unrelated application treats methods differently, investigate the underlying authorization rather than inferring a bypass from metadata alone.

Cleanup: no fixture change occurs. Close the lab browser and restore manually changed proxy settings when finished.


## 22. Worked example: Three-path ffuf exercise and false-positive analysis

Question: which entries in a short known list exist? Use practice-paths.txt from this download.

```sh
ffuf -w practice-paths.txt -u http://127.0.0.1:8765/FUZZ -t 1 -rate 1 -maxtime 15 -mc all
```

Expected on the supplied fixture: marker.txt is 200, training-status.json is 200, and missing-training-file.txt is 404. Correlate each with the server access log and inspect its body with curl. The JSON record is deliberately public training data; no authentication or real customer data exists here.

Worked reasoning: a 200 response shows a returned resource, not an access-control failure. On a different app, a soft-404 might return 200 for every path, so compare negative-control content before interpreting discoveries. Do not increase concurrency or add recursive discovery merely because the tool supports it.

Cleanup: the tool does not modify fixture files. Record the exact three inputs and observed statuses, then stop the server after all exercises.


## 23. Worked example: Query strings: input acceptance versus meaningful processing

Question: does adding a parameter mean the server acted on it? Compare these requests in curl or Burp Repeater.

```sh
curl --max-time 5 -i "http://127.0.0.1:8765/marker.txt?mode=preview"
curl --max-time 5 -i "http://127.0.0.1:8765/marker.txt?mode=unknown"
```

Expected for Python SimpleHTTPRequestHandler: both return the same marker because file lookup does not implement this application parameter. The query can still appear in the access log. A 200 response therefore does not prove a feature exists or that the parameter was validated.

Practice: annotate your evidence with the server implementation and compare bodies, not just status codes. Do not call this an authorization bypass; the fixture has no mode-based access restriction. For a real owned test app, define the intended parameter behavior before varying it.

Cleanup: these requests change no persistent application state; no session was created.


## 24. Worked example: Correlate Nmap, curl and defender evidence

Question: what claim does each observation support? Start with the bounded port check, then retrieve the marker.

```sh
nmap -sT -p 8765 --reason 127.0.0.1
curl --max-time 5 -i http://127.0.0.1:8765/marker.txt
```

Build a three-row evidence table in your notes. Nmap supports TCP reachability from this source. curl supports receipt of the specific HTTP response. The server log supports observation of the request by this process. The initial connect scan may not generate a normal HTTP request log entry because it need not send an HTTP request.

Advanced question: where would an EDR, proxy or SIEM see these actions? Mark collection untested unless you actually configured and checked that sensor. An absent SIEM alert is not evidence of stealth when no ingestion was set up.

Cleanup: stop the fixture; preserve timestamps with timezone context and distinguish operator time from sensor time.


## 25. Worked example: Two-user authorization test plan for an owned application

This is a worked planning example, not an executable test against the static fixture. Prerequisites: your own staging app, two synthetic accounts and a resettable test dataset. The supplied JSON is public and cannot test access control.

Create a private test note as account A. Establish that A can read it and B can read B own note. In an authorized Burp test session for B, request the A test-note identifier once using the app normal request format. Avoid collecting any unrelated records.

Expected: B receives the application documented denial, often 403 or a deliberately indistinguishable 404, with no A note content. A 200 containing a generic error is not necessarily unauthorized access; inspect content and server authorization evidence.

If the A note is returned, record the two account roles, resource ownership, minimal request and sanitized response. Suggested remediation: enforce ownership on the backend, then retest both denied cross-account access and permitted own-account access. Cleanup: remove only your synthetic records and test sessions through the app normal controls.


## 26. Worked example: Identity-path tabletop and remediation retest

Use this fictional relationship chain for a BloodHound-style reasoning exercise: trainee-a belongs to Support-Test; Support-Test can reset the password of service-test; service-test has access to a synthetic reporting resource. No dataset or collector is required for this tabletop.

For each edge, write the source of evidence and prerequisite: group membership, effective delegated permission, account state, and actual resource authorization. A drawn path does not prove that policy permits every operation. Do not attempt password resets merely to demonstrate the diagram.

Propose removing an unnecessary reset delegation while preserving required support tasks. In a separately prepared lab, compare effective permissions and a refreshed graph after the approved change, then check legitimate support access. An old graph may still show the removed edge.

Output: one conditional risk statement and one retest plan with an owner. Cleanup: no account or permission is changed by this tabletop.


## 27. Worked example: Purple-team result and report: a complete worked example

Objective: confirm visibility of a harmless local marker request. Starting condition: an operator on the same machine as the loopback Python server. Action: one GET for marker.txt.

Observed: client receives 200 and the known marker; the server records the requested path and status. Conclusion: the fixture is reachable from loopback and the process logged the request. Unproven: external reachability, enterprise egress controls, SOC detection, account compromise or access to sensitive information.

A useful next step is an approved lab pipeline that ingests the server event and routes a training case to the SOC. Success criteria should include correct fields, timestamps, case owner and a documented analyst decision, not merely rule firing.

Cleanup evidence: the server process was stopped; a subsequent request cannot retrieve the marker from that process. If another process owns the port, stop testing and identify it. Record any generated response files and their retention decision.

Deliverables: operator timeline, sensor evidence, explicit limitations and an assigned follow-up. This example demonstrates accurate reporting of a normal observation rather than inventing a vulnerability.
