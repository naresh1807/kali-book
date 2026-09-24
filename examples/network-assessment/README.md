# Network penetration testing: local workbook

## Study route and prerequisites

Use the network studies in Chapters 16, 18, 19, 20, 21 and 35. Commands below are Kali Bash examples. Install the named tools separately if needed; the website does not execute commands. Download and extract the examples ZIP, then copy examples/network-assessment into ~/kali-lab/network-assessment in Kali. A Windows drive is not automatically mounted inside a VM.

The practical targets are loopback services you start yourself. The evidence exercise is entirely offline. No physical devices, other computers, internet services or firewall rules are probed or modified by these examples.

## Offline segmentation-evidence lab

```sh
cd "$HOME/kali-lab/network-assessment"
python3 flow_review.py
python3 -m unittest -v test_flows
```

Python 3.10+ standard library only. Expect six outcomes in order: pass, fail, pass, inconclusive, inconclusive, fail; ten tests pass. A zero demonstration exit code means the deliberately mixed evidence was classified correctly, not that every flow passed. Documentation addresses are fictional.

reachable means a confirmed TCP connection; policy_blocked assumes independently verified applicable firewall evidence, not a guessed timeout; closed means a verified closed TCP listener; timeout remains unknown. The model does not validate these observations itself. It evaluates transport reachability only, not user permissions, application identity, UDP, IPv6 or real firewall configuration. In a copy of flows.json, change expected/observed values and explain the new verdicts; the demonstration's fixed expected-result check will then need deliberate adjustment.

## Local configuration: ip and ss

```sh
ip -brief address show lo
ip route get 127.0.0.1
ss -ltn 'sport = :8910'
```

The interface command inspects loopback; the route command asks the local kernel for a path without probing a remote service; ss lists local TCP listeners on the selected port. Run ss before and after starting the next fixture. If that port already belongs to another process, select a free port consistently rather than stopping an unknown service. Do not copy real workstation interface output into the public handbook.

## Nmap and curl: one local service

Terminal A, from the network-assessment folder:

```sh
python3 -m http.server 8910 --bind 127.0.0.1 --directory site
```

Terminal B:

```sh
nmap -sT -Pn -n -p 8910 --reason --max-retries 1 --host-timeout 15s 127.0.0.1
curl --silent --show-error --max-time 5 -i http://127.0.0.1:8910/
```

Expect the configured TCP port to be open and HTTP to return 200 with the fictional page. -sT requests TCP connect scanning, -Pn skips host discovery, -n skips DNS lookup and -p selects exactly one port. The other options expose reasons and bound retries/runtime. These bounds can reduce confidence on a slow path. The displayed service label without version detection may come from a port database; the curl response independently establishes the HTTP exchange.

Stop Terminal A with Ctrl+C, verify its listener is gone with ss, then repeat Nmap. A closed result is expected if no other process took the port and local filtering does not obscure it. A timeout requires investigation. An open port is not by itself a vulnerability.

## Ncat and tcpdump: a bounded plaintext exchange

First choose a free port 9099 and create an evidence directory. Terminal A:

```sh
mkdir -p evidence
ncat --listen 127.0.0.1 9099
```

Terminal B, from the same folder:

```sh
sudo timeout 20s tcpdump -i lo -nn -s 0 -c 40 -w evidence/local.pcap 'tcp port 9099'
```

Immediately use Terminal C:

```sh
ncat 127.0.0.1 9099
```

Type a fictional greeting and press Enter; reply from Terminal A. End the connection with Ctrl+C and allow capture to stop. No shell execution is attached to Ncat. --listen creates a local listener; the client uses connect mode. tcpdump selects loopback, avoids name lookup, records full packets, limits count and writes a file. timeout also bounds the capture window; its timeout exit status is not automatically a capture failure. Do not write real passwords into this plaintext exchange.

## Wireshark and TShark: interpret the saved trace

```sh
tcpdump -nn -r evidence/local.pcap
tshark -r evidence/local.pcap -Y 'tcp.port == 9099' -T fields -e frame.number -e ip.src -e tcp.flags -e tcp.len
```

Open the same file in Wireshark and apply tcp.port == 9099 as a display filter. Locate SYN, SYN/ACK, ACK, payload and connection close if captured. Follow TCP Stream reconstructs the visible plaintext exchange; it does not decrypt arbitrary TLS traffic. tcpdump capture syntax 'tcp port 9099' is different from Wireshark display syntax 'tcp.port == 9099'. A display filter hides packets from view without deleting them from the capture.

If the file is empty, verify capture began before the exchange and the interface/port match. A partial capture may miss the handshake. Loopback does not exercise a physical switch, router or radio.

## iperf3: bounded throughput demonstration

Terminal A:

```sh
iperf3 -s -B 127.0.0.1 -p 5202 -1
```

Terminal B:

```sh
iperf3 -c 127.0.0.1 -p 5202 -t 3 -b 1M
```

The server binds only to loopback and exits after one client test. The client runs a three-second TCP test with a target rate of one megabit per second. The observed rate can differ from the target; inspect both ends. This measures local stack/host behavior, not internet speed or a physical network link. Verify the one-shot server exited afterward.

## DNS and TLS: separately configured prerequisites

The new workbook does not include a DNS server, certificate authority or TLS listener. Use the commands below only after configuring your own corresponding lab service; failure without those prerequisites is expected.

```sh
dig @127.0.0.1 -p 5353 lab.example.test A +time=2 +tries=1
openssl s_client -connect 127.0.0.1:9443 -servername lab.example.test -verify_hostname lab.example.test -verify_return_error -CAfile lab-ca.pem </dev/null
```

DNS requires a local server on port 5353 and a known lab zone; inspect response code, server and answer. TLS requires a local listener on 9443, a certificate for lab.example.test and the correct lab-ca.pem trust file. SNI and hostname verification have distinct purposes. Do not disable certificate validation just to obtain a successful result. Neither command contacts a public example domain.

## Service and vulnerability tool selection

Use OpenSSH clients for a configured SSH service, smbclient for approved share access, and SNMP utilities for a known protected management service. Credentials and permission to read each resource are prerequisites. Compare an allowed resource with a denied one; avoid password guessing as a default test.

Nmap service probes, reviewed NSE scripts and credentialed vulnerability scanners can generate candidate findings. They send additional traffic beyond port checks. Confirm vendor build, configuration and actual feature exposure before reporting a CVE. Inspect script behavior and authentication success; a clean report may simply mean the scanner lacked access.

Wireshark examines traffic; Scapy can parse saved packets or generate packets, which are different activities requiring different scope. Directory relationship tools and wireless tools need separately defined labs and data-handling plans. No single tool establishes complete network security.

## Evidence, cleanup and retest worksheet

Source zone | destination asset | protocol/port | expected reachability | observation | supporting listener/policy evidence | verdict | repair | retest.

Classify timeouts as inconclusive until evidence resolves them. A closed service does not prove a firewall blocks an active listener. After a policy repair, confirm required clients still connect. Record application authorization separately from transport access.

Stop only the lab processes you started, confirm their listeners closed, and store captures with appropriate access restrictions. The supplied files contain no personal host information.

References: [Nmap](https://nmap.org/book/man.html), [Ncat](https://nmap.org/ncat/guide/), [Wireshark](https://www.wireshark.org/docs/wsug_html_chunked/), [tcpdump](https://www.tcpdump.org/manpages/tcpdump.1.html), [iperf3](https://software.es.net/iperf/invoking.html), [OpenSSL](https://docs.openssl.org/master/man1/openssl-s_client/).
