# Advanced network attack analysis: offline workbook

This workbook examines mechanisms, prerequisites and evidence. It does not transmit attack traffic, collect credentials or change routes. The six scenarios in scenarios.json are fictional. Read each evidence statement, answer the question, then compare your reasoning with the supplied answer. No packages are required to read the files.

## Separate stages before drawing conclusions

For each proposed path record: attacker position -> controllable input -> trust decision -> accepted effect -> resulting capability. Mark every stage observed, inferred or unknown. Add a benign alternative explanation and the minimum extra evidence needed to distinguish it. Then choose one control that breaks the path and one legitimate operation that must still work.

## Wireshark and TShark on an approved capture

These commands require your own authorized saved capture named approved-lab.pcap; no capture is bundled. A loopback TCP trace from the earlier network lab will not contain ordinary Ethernet ARP or a switched-network attack.

```sh
tshark -r approved-lab.pcap -Y 'arp'
tshark -r approved-lab.pcap -Y 'dns || llmnr || nbns'
tshark -r approved-lab.pcap -Y 'tcp.flags.syn == 1' -T fields -e frame.number -e ip.src -e ip.dst -e tcp.dstport
```

-r reads an existing file and -Y applies a display filter; these commands do not capture or inject traffic. Protocol decoding and field support depend on the installed version and capture contents. Open the same trace in Wireshark and correlate frames with host and switch logs. A filter match identifies matching packets, not automatically an attack. Do not share real credential-bearing capture content.

## Tool capabilities and boundaries

Use Wireshark/TShark for evidence interpretation and Nmap for the already documented exact-port localhost observations. Scapy supports both offline parsing and packet transmission; those modes have different effects. Responder and Bettercap can introduce active local-network behavior, and Impacket contains protocol and authentication utilities with widely varying effects. Review a specific function rather than assuming a whole toolkit is passive or harmless.

No active poisoning, relay, credential-guessing, wireless disruption or flooding commands are part of this offline workbook. For a separately authorized active lab, define test identities, target services, traffic budgets, recovery and observable success/failure conditions before selecting a tool. Production telemetry review and configuration validation often answer the question without reproducing an attack.

## Control-validation matrix

Technique | required attacker position | receiver trust decision | observed evidence | benign explanation | blocked transition | allowed operation after repair | residual uncertainty.

ARP example: local-link presence -> neighbor mapping accepted -> confirm both mapping and packet path -> legitimate gateway failover alternative -> validated switch binding policy -> legitimate gateway traffic works -> encrypted application content may remain unreadable.

Relay example: authentication exchange available -> destination accepts it in another context -> correlate destination action -> rejection or unrelated login alternative -> protocol-appropriate integrity/binding protection -> approved client still authenticates -> other protocols need separate review.

## Report the outcome accurately

Use attempt, accepted redirection, authenticated operation and confirmed impact as separate descriptions. A diagram, tool name or technique identifier is not proof of all stages. Record missing telemetry and unsupported assumptions. Keep assessment activity scoped to owned or explicitly authorized systems.

References: [MITRE name-resolution poisoning and relay](https://attack.mitre.org/techniques/T1557/001/), [SMB signing](https://learn.microsoft.com/windows-server/storage/file-server/smb-signing-overview), [Source-address validation](https://www.rfc-editor.org/info/rfc2827/), [Wireshark guide](https://www.wireshark.org/docs/wsug_html_chunked/).
