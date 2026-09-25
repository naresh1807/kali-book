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
