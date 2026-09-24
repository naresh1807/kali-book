# Remote access: concepts and tool workbook

## Prerequisites and offline inspection

Extract examples/remote-access from the lab ZIP. The sample configuration is a text file for an OpenSSH client. It does not create an account, start a service or change firewall rules. Commands are Kali Bash examples unless labelled Windows. No real credentials are included.

```sh
ssh -V
ssh -F ssh-lab.conf.txt -G lab-ssh
```

-F selects only the supplied configuration file; -G prints the evaluated configuration and exits without connecting. Expect hostname 127.0.0.1, port 2222, user labuser, agent forwarding disabled and a five-second connection timeout. Some display spellings vary by client version. The supplied file contains no Include or Match-exec directives. Inspect configuration before using files from elsewhere.

## SSH terminal: separately configured local server

This needs an SSH server you configured on 127.0.0.1:2222, a labuser account, authentication credentials and a known server fingerprint. None is provisioned by the book.

```sh
ssh -F ssh-lab.conf.txt lab-ssh
```

Verify any first-use host-key prompt against the trusted server fingerprint before accepting. Use exit to close the shell when finished. If the server is absent, connection refusal is expected; do not interpret it as a failed account test. Do not disable host verification to make the connection succeed.

For troubleshooting the same configured fixture:

```sh
ssh -v -F ssh-lab.conf.txt lab-ssh
```

Verbose output can reveal usernames and local paths; redact it before sharing. Connection setup timeout and keepalive settings serve different purposes and are not an absolute session lifetime policy.

## Local forwarding: client and server perspectives

Requires the same SSH server, forwarding permission and an explicitly approved fictional HTTP service reachable from that server at 127.0.0.1:8910. You can configure that HTTP fixture using the network-assessment workbook on the SSH server. Choose a free client port 8899.

Terminal A:

```sh
ssh -F ssh-lab.conf.txt -N -L 127.0.0.1:8899:127.0.0.1:8910 lab-ssh
```

Terminal B:

```sh
curl --silent --show-error --max-time 5 -i http://127.0.0.1:8899/
```

-N requests no remote command. -L binds client loopback port 8899 and routes connections over SSH to server-side loopback port 8910. The second 127.0.0.1 is interpreted from the SSH server's network context. Expected result is the synthetic HTTP page if all prerequisites are met. A tunnel established successfully can still fail when its backend is unavailable. The sample ExitOnForwardFailure does not guarantee backend availability. Ctrl+C in Terminal A stops the forward; confirm the local listener closes. No remote forwarding or public listener is created.

## SFTP: controlled file access

```sh
sftp -F ssh-lab.conf.txt lab-ssh
```

After authenticating to the configured local server, use pwd and ls to inspect the permitted lab directory and bye to disconnect. Use only synthetic files for any upload/download exercise and keep output names separate from existing evidence. Account permissions still apply. A valid SSH identity is not permission to read every remote path.

## RDP clients and gateways

On Windows, the following opens the Remote Desktop Connection client UI:

```text
mstsc
```

Enter only your separately configured owned host and intended gateway. Check certificate identity, Network Level Authentication support, authorized users and redirection settings. This command does not enable Remote Desktop hosting. On Kali, Remmina or FreeRDP can be used with a configured service; inspect installed client help rather than copying credentials into shell arguments. Features vary by client/server edition and policy.

RD Gateway provides an authenticated path to selected RDP resources; VPNs provide a different network access model. MFA integration depends on the deployment, not simply on using RDP or NLA. Test clipboard and drive redirection requirements deliberately.

## VPN and access-policy worksheet

For an already configured WireGuard client, this command shows runtime status without changing its configuration:

```sh
wg show
```

It may require permission and can display peer identifiers and endpoint addresses; do not publish the raw output. A recent handshake confirms peer communication, not application authorization or correct DNS/routing. Use approved client settings for WireGuard or OpenVPN instead of inventing production keys, endpoints or routes.

Record: peer identity, expected routes, split/full tunnel policy, IPv4/IPv6 coverage, DNS resolver behavior, allowed service, denied service, authentication method and revocation procedure. Avoid confusing AllowedIPs with a complete firewall or user-permission policy.

## Remote-access verification worksheet

Actor | client | gateway | target resource | expected operation | observed result | evidence | revocation check.

1. Verify the intended server identity before entering credentials.
2. Confirm one approved operation works under a non-administrator lab account.
3. Confirm a separate resource or operation outside that account's policy is denied.
4. Close the session and confirm temporary forwarding/listeners are gone.
5. Revoke a temporary credential in the configured lab and test new-login denial. Check existing-session termination separately.
6. Preserve redacted audit evidence and explain any untested controls.

No server, VPN, RDP endpoint or remote account is enabled by this workbook. It teaches explicit administration paths with authenticated identities and scoped access.

References: [OpenSSH client](https://man.openbsd.org/ssh), [WireGuard](https://www.wireguard.com/quickstart/), [Microsoft RD Gateway](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop%2Dservices/remote-desktop%2Dgateway-role).
