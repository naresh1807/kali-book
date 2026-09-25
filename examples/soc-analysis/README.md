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
