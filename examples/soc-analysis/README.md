# SOC analyst workbook

## 1. Start with a question

This offline lab uses fictional authentication events in an in-memory SQLite database. It makes no network connection and changes no accounts. It teaches grouping, a bounded event-time window and evidence limits; it is not a production detector or SIEM integration.

From this extracted folder, run:

```sh
python3 auth_triage.py
python3 -m unittest -v test_auth_triage.py
```

On Windows, use python if python3 is unavailable. Expect trainee-a with three failures. This is a lead to investigate, not a confirmed incident. The fixture also contains a success, a different user, an older failure and a later event.

## 2. Query and investigation workflow

The query counts failure records per account between a supplied start and end, inclusive. Timestamps use identical UTC ISO formatting so lexical order is meaningful. Do not apply this assumption to mixed timezones or formats. The example uses a fixed evaluation window, not a continuously running sliding-window engine.

Read the query in auth_triage.py. Change the threshold and window in a copy. Explain why a success does not cancel a failure count and why a different account must not be merged into trainee-a. Real systems need duplicate handling, event validation, ingestion-delay policy and entity context.

After a match, ask: Is the account privileged? Was a reset underway? Which devices were involved? Did an unusual success occur? Which session or endpoint evidence could confirm misuse? Record missing evidence explicitly.

## 3. Tools and query translation

Microsoft Sentinel and Defender use KQL in relevant query experiences; Splunk uses SPL; Elastic supports its own search and query interfaces. Verify the actual schema and time semantics before translating the SQLite logic. Tool syntax is not interchangeable.

Wazuh can support endpoint collection and detection. EDR provides process and host context. Zeek produces network metadata, Suricata supplies network detection and protocol events, and Wireshark inspects captures. Visibility depends on sensor placement and configuration.

Sigma helps describe detection logic for supported backends. Validate field mapping and converted queries against fixtures. SOAR and case-management platforms organize enrichment, decisions and handovers; they do not replace incident ownership.

## 4. Case and handover template

Alert and rule version:
Evaluation window and ingestion delay:
Affected account, asset and business context:
Observed facts and evidence locations:
Hypothesis and alternative explanations:
Severity, confidence and priority rationale:
Missing evidence and next queries:
Escalation owner and deadline:
Containment decision, authorization and rollback:
Disposition, remediation and retest:
Handover owner and next action:

## 5. Sources and progression

[NIST incident response guidance](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
[MITRE ATT&CK detection strategies](https://attack.mitre.org/detectionstrategies/)
[MITRE ATT&CK data components](https://attack.mitre.org/datacomponents/)
[Microsoft Sentinel documentation](https://learn.microsoft.com/azure/sentinel/)
[Sigma documentation](https://sigmahq.io/docs/)
[Zeek documentation](https://docs.zeek.org/)
[Suricata documentation](https://docs.suricata.io/)

Study lessons 01-08 for foundations, 09-16 for investigations and response, and 17-24 for detection engineering and advanced operations. Tests validate only the supplied offline query behavior; no enterprise platform was deployed or tested.


## 6. Python, SQLite and jq: start offline

Purpose and setup: Python 3 includes SQLite; use the extracted soc-analysis folder. jq is an optional JSON command-line tool installed separately. No SIEM account is needed.

```sh
python3 auth_triage.py
python3 -m unittest -v test_auth_triage.py
jq -s '[.[] | select(.outcome == "failure" and .ts >= "2026-01-01T09:55:00Z" and .ts <= "2026-01-01T10:00:00Z")] | group_by(.account) | map({account: .[0].account, failures: length}) | map(select(.failures >= 3))' auth-events.jsonl
```

How it works: -s reads JSON lines into an array. select filters outcome and the inclusive UTC window. group_by separates accounts; length counts their events. The final select applies the threshold. Expected: trainee-a with 3 failures. Lexical timestamps work here because every fixture uses the same UTC format.

Practice: raise the threshold to 4 and expect no matches. Lower it to 1 and expect trainee-a with 3 and trainee-b with 1. Neither result establishes an incident. The supplied Python tests check the fixture query, not jq itself.

Reference: https://jqlang.org/manual/


## 7. Microsoft Sentinel and KQL: synthetic search

Setup: use an authorized workspace with a KQL query experience, such as Azure Monitor Logs used with Sentinel. Workspace access and permissions are prerequisites; no workspace is created by the handbook. Choose the KQL editor, not a different query mode.

Paste sentinel-query.txt into a new query and run it. This datatable generates temporary synthetic rows without onboarding logs.

```kusto
datatable(EventTime:datetime, Account:string, Outcome:string)
[
 datetime(2026-01-01T09:54:59Z), "trainee-a", "failure",
 datetime(2026-01-01T09:55:00Z), "trainee-a", "failure",
 datetime(2026-01-01T09:57:00Z), "trainee-a", "failure",
 datetime(2026-01-01T10:00:00Z), "trainee-a", "failure",
 datetime(2026-01-01T09:59:00Z), "trainee-a", "success",
 datetime(2026-01-01T09:58:00Z), "trainee-b", "failure",
 datetime(2026-01-01T10:00:01Z), "trainee-a", "failure"
]
| where EventTime between (datetime(2026-01-01T09:55:00Z) .. datetime(2026-01-01T10:00:00Z))
| where Outcome == "failure"
| summarize Failures=count() by Account
| where Failures >= 3

```

How it works: datatable defines typed columns; between includes both window endpoints; summarize counts per Account. Expected: one row, trainee-a and 3. Change the last threshold to 4 for a negative control.

For real data: identify the actual table and fields, inspect a small time-bounded sample, then translate this logic. Do not assume every tenant has SigninLogs or the same connectors. Save a query first; creating a scheduled rule additionally needs frequency, lookback, entity mapping, duplicate policy and an owner.

Reference: https://learn.microsoft.com/kusto/query/datatable-operator


## 8. Splunk and SPL: search before alerting

Setup: use an authorized Splunk Search & Reporting search editor with SPL support. Paste splunk-query.txt and run it. makeresults creates a synthetic result in search memory and does not index these events.

```spl
| makeresults
| eval rows=split("2026-01-01T09:54:59Z,trainee-a,failure;2026-01-01T09:55:00Z,trainee-a,failure;2026-01-01T09:57:00Z,trainee-a,failure;2026-01-01T10:00:00Z,trainee-a,failure;2026-01-01T09:59:00Z,trainee-a,success;2026-01-01T09:58:00Z,trainee-b,failure;2026-01-01T10:00:01Z,trainee-a,failure", ";")
| mvexpand rows
| eval parts=split(rows, ",")
| eval ts=mvindex(parts,0), account=mvindex(parts,1), outcome=mvindex(parts,2)
| eval _time=strptime(replace(ts,"Z$","+0000"),"%Y-%m-%dT%H:%M:%S%z")
| where _time >= strptime("2026-01-01T09:55:00+0000","%Y-%m-%dT%H:%M:%S%z") AND _time <= strptime("2026-01-01T10:00:00+0000","%Y-%m-%dT%H:%M:%S%z")
| search outcome="failure"
| stats count AS failures BY account
| where failures >= 3

```

How it works: split creates event and field lists; mvexpand makes one row per fixture event. strptime explicitly parses the UTC offset. where bounds event time; stats groups by account. Expected: trainee-a and failures=3. Raising the threshold to 4 should remove the result.

For real data: replace the synthetic source with your authorized index and sourcetype, confirm account/outcome extraction and bound time before aggregating. Save as a search first. Scheduling an alert additionally requires throttling, routing and ownership; do not enable automated containment from this demonstration.

Reference: https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.0/search-commands/makeresults


## 9. Elastic Security and Kibana: inspect events

Setup: use an authorized lab deployment, an existing log index and a data view that exposes the required fields. Discover uses the selected query mode; Kibana Query Language is different from Microsoft Kusto Query Language despite the shared KQL abbreviation.

In Discover, select the correct data view, set a small absolute time range and add timestamp, user and outcome columns. If your lab data uses Elastic Common Schema, try this Kibana filter:

```text
event.category: authentication and event.outcome: failure
```

Expected: only matching events within the UI time range. Missing fields or a different schema can produce zero rows; inspect a known event before concluding there was no activity. Expand one row to see its raw fields. Build a user-count visualization only after confirming the filter. This filter does not implement the five-minute threshold by itself.

Practice: compare a known success event and failure event. Record the index, time picker and field mappings in your case. Creating detection rules is a separate configuration step requiring testing and privileges.

Reference: https://www.elastic.co/docs/explore-analyze/query-filter/languages/kql


## 10. Wazuh: decoder and rule testing

Setup: use an existing owned Wazuh lab server. The logtest command belongs on the server, not an ordinary agent. This exercise uses a synthetic JSON event; it does not require generating failed logins.

```sh
sudo /var/ossec/bin/wazuh-logtest
```

Paste this single line, then press Enter:

```json
{"integration":"soc-training","account":"trainee-a","outcome":"failure","training":true}
```

Inspect decoding output for the account and outcome fields. A matching alert is not guaranteed because installed rules may not select this custom event. Read the matched rule description and level, if any. Ctrl+C exits.

Practice: change outcome to success and compare decoding. A custom rule should be reviewed in a lab and tested with both inputs before deployment. Repeated-failure correlation requires frequency and timeframe logic, not just a JSON field match. logtest success does not prove an agent-to-dashboard pipeline works.

Reference: https://documentation.wazuh.com/current/user-manual/ruleset/testing.html


## 11. Event Viewer, PowerShell and Sysmon: endpoint evidence

Setup: on your own Windows lab host, open Event Viewer and choose the Security log. Reading it may require elevated access and suitable auditing. The following read-only PowerShell query limits collection to the last hour and at most 20 failed logon events.

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddHours(-1)} -MaxEvents 20 | Select-Object TimeCreated, Id, ProviderName, Message
```

Expected: matching events, or a no-events/error result if none exist, auditing is absent or access is denied. Inspect logon type, target account, status and source fields; failure alone does not establish guessing. Do not create production failures merely to populate the view.

If Sysmon is already configured on a lab host, inspect its Microsoft-Windows-Sysmon/Operational log. Process creation (event 1) and network connection (event 3) visibility depends on configuration; network events are not universally enabled. Correlate process identity and time with EDR evidence, and do not assume a missing event proves absence.

Practice: build a timeline from a benign lab process and redact usernames, paths and addresses before sharing it. Installing or reconfiguring Sysmon changes collection and is outside this read-only exercise.

Reference: https://learn.microsoft.com/en-us/powershell/scripting/samples/creating-get-winevent-queries-with-filterhashtable
Reference: https://learn.microsoft.com/sysinternals/downloads/sysmon


## 12. Wireshark and TShark: read a packet capture

Setup: install Wireshark/TShark from their official distribution and supply an authorized, non-sensitive capture named lab.pcap. No capture is included. These commands read a file rather than capturing live traffic.

```sh
tshark -r lab.pcap -Y "dns" -T fields -e frame.number -e dns.qry.name
tshark -r lab.pcap -Y "tcp.flags.syn == 1 && tcp.flags.ack == 0" -T fields -e frame.number -e ip.src -e ip.dst -e tcp.dstport
```

-r selects the file, -Y applies a display filter, -T fields selects tabular output and -e chooses columns. The second command shows initial TCP SYN packets; ip.src/ip.dst may be empty for IPv6 traffic. Add ipv6.src and ipv6.dst where relevant.

GUI workflow: open the capture, apply dns in the display-filter bar, inspect query/response pairs and packet timestamps. Expected results depend on the capture; encrypted DNS may not appear as ordinary DNS. A SYN does not establish a successful connection.

Practice: find one request and its response, then document what the capture cannot show. Do not confuse display filters with capture filters.

Reference: https://www.wireshark.org/docs/man-pages/tshark


## 13. Zeek: turn a capture into metadata

Setup: install Zeek separately, add its binaries to PATH and supply an authorized lab.pcap. Use a fresh empty output directory so earlier logs cannot be mistaken for new results. Run these in a Linux shell from the folder containing the capture.

```sh
mkdir zeek-output
cd zeek-output
zeek -r ../lab.pcap
zeek-cut ts id.orig_h id.resp_h service < conn.log
```

-r reads saved traffic and writes logs in the current directory. With default tab-separated logs, zeek-cut selects named columns. If JSON logging is configured, use a JSON parser instead. conn.log or dns.log exists only when the analyzed traffic and policy generate it.

Expected: connection metadata when supported traffic is present. Inspect timestamps, endpoints and protocol evidence; metadata is not full application content. Review reporter or diagnostic output if expected traffic is missing. Do not automatically ignore checksum errors without understanding capture offload effects.

Practice: correlate one conn.log entry with the same flow in Wireshark. Record tool version, capture hash and configuration.

Reference: https://docs.zeek.org/en/current/quickstart.html


## 14. Suricata and jq: inspect network detections

Setup: use an existing lab installation with a known suricata.yaml and reviewed ruleset. Supply lab.pcap. The configuration path below is a common Linux location; verify your installation. Use a new output directory.

```sh
mkdir suricata-output
suricata -T -c /etc/suricata/suricata.yaml
suricata -r lab.pcap -c /etc/suricata/suricata.yaml -l suricata-output
jq 'select(.event_type == "alert") | {timestamp, signature: .alert.signature, severity: .alert.severity}' suricata-output/eve.json
```

-T validates configuration; stop if it fails. -r reads the saved capture and -l chooses the output directory. Reading a file does not require configuring an inline blocking deployment. The jq query selects alert records from EVE JSON when that output is enabled.

Expected: alerts only when loaded rules match the capture. Zero alerts can mean no match, disabled rules, unsuitable traffic or missing output configuration. Check startup messages, packet statistics and rule loading before interpreting results. An alert signature is a lead, not a final incident verdict.

Practice: compare one alert with its underlying packet and document the rule, evidence and plausible benign explanation.

Reference: https://docs.suricata.io/en/suricata-7.0.11/command-line-options.html


## 15. Sigma: detection intent to tested queries

Setup: install sigma-cli in a separate environment if you want to convert rules. Backends and processing pipelines are separate dependencies; check your installed help and the official guide before selecting them.

```sh
sigma --help
sigma plugin list
sigma convert --help
```

Workflow: choose a reviewed rule for a data source you actually collect. Read logsource, detection selection, condition, falsepositives and level. Identify the required event fields. Select a compatible backend and mapping pipeline, convert in a lab, then inspect the generated query before running it against fixtures.

Expected: a query after successful conversion, not proof that the query detects the intended behavior. A single-event selection does not automatically implement time-window correlation. Test positive, negative, missing-field and boundary cases and record rule and backend versions.

Practice: express the authentication example as a detection specification first: failed outcome, account grouping, inclusive five-minute window, count at least three. Verify your selected rule type/backend supports that correlation rather than silently replacing it with a simple match.

Reference: https://sigmahq.io/docs/guide/getting-started.html


## 16. CyberChef: decode and explain an artifact

Setup: use a trusted CyberChef deployment; for confidential evidence use an approved local build. The supplied value is harmless synthetic text. No external enrichment is needed.

Paste U09DLVRFU1Q= into Input. Add From Base64 to the recipe. Expected output: SOC-TEST. Save the recipe alongside the input and explanation if recording the exercise.

How it works: Base64 represents bytes as text. Successful decoding does not establish encryption, intent or malicious behavior. Choose the correct character encoding when rendering bytes. Do not execute decoded commands or open extracted links as part of decoding.

Practice: compare the original and decoded representation, then explain why an encoded string alone is a weak detection signal.

Reference: https://github.com/gchq/CyberChef


## 17. Case management and SOAR: evidence to action

Setup: use an approved lab case platform such as TheHive, or start with the supplied workbook template. UI labels and integrations vary; use a synthetic case and disable outbound response actions during practice.

Step 1: create a case titled Training authentication threshold. Record trainee-a, the UTC window, rule logic and the three matching failures. Mark it as a training case.

Step 2: add tasks for validating device context, checking a password reset explanation and reviewing related successes. Assign owners and deadlines. Record facts separately from hypotheses.

Step 3: design a dry-run playbook in your approved SOAR platform: validate input, enrich from a local mock inventory, attach results, propose priority and request an authorized containment decision. A missing account or failed enrichment should stop that branch and create a review task.

Step 4: replay the same alert twice. Expected: one linked case or deduplicated update, not duplicate containment. Keep action logs and explicit rollback steps before enabling any real response integration.

Practice: complete the handover template and explain why a threshold match alone does not justify disabling an account. No external cases, notifications or integrations are created by this handbook.

Reference: https://docs.strangebee.com/thehive/

The Python/SQLite fixture is tested locally. KQL, SPL and other product-specific examples are documented manual exercises and have not been executed against those products. No SOC tools are installed by reading or downloading this book.
