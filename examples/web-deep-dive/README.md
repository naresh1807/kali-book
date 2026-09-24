# Deep web testing: local workbook

## Offline code lab

Use Python 3.10+ with its standard library. From this extracted directory:

```sh
python3 boundary_lab.py
python3 -m unittest -v test_boundaries
```

Expect eight true demonstration results and fourteen passing tests. Windows may use `python` instead of `python3`. No sockets open, no external database is accessed, and no credentials are needed. The SQLite database exists only in memory and has three fictional records.

1. Explain why the same input expands an unsafe query but is treated literally by the bound query. Find the exact line where data crosses into SQL syntax.
2. Explain why a legitimate apostrophe must continue to work after the repair. Parameterization does not replace application authorization: the caller identity must still come from a trusted authentication layer.
3. Compare a markup-looking string with its HTML-text-encoded representation. This test does not run a browser or prove JavaScript, URL or CSS contexts safe.
4. Draw draft -> paid -> fulfilled. Explain why draft -> fulfilled is rejected. The state function assumes an authorized caller and trusted payment event; it has no payment provider, persistent state, atomic transaction or concurrency control.
5. Write one finding with baseline, changed input, observed effect, root cause, repair and allowed/denied retest results. The intentional vulnerable functions are negative controls, not production helpers.

## Tool prerequisites and working directory

The commands below are for Kali Bash, with each named tool installed separately. Copy the examples folders as siblings under ~/kali-lab. Open a new folder or save a copy before editing a supplied fixture. Review installed `--help` output if your version differs. No package installation or remote scanning is performed by these instructions.

Terminal A, HTTP header fixture:

```sh
python3 "$HOME/kali-lab/web-programs/fixture_server.py" --port 8891
```

Terminal B:

```sh
cd "$HOME/kali-lab/web-deep-dive"
curl --version
ffuf -V
gobuster version
nuclei -version
semgrep --version
```

Missing optional tools do not prevent the offline Python exercises. Ctrl+C stops Terminal A when finished.

## curl: one request, one question

```sh
curl --silent --show-error --max-time 5 -i http://127.0.0.1:8891/strong
curl --silent --show-error --max-time 5 -i http://127.0.0.1:8891/weak
curl --silent --show-error --max-time 5 -i http://127.0.0.1:8891/redirect
curl --silent --show-error --max-time 5 -i -H 'Origin: https://review.invalid' http://127.0.0.1:8891/cors
```

Expected: /strong and /weak return 200 with different security headers; /redirect returns 302 and Location /strong; /cors reflects the synthetic Origin and declares credentials allowed. The Origin value is a header string, not a destination contacted by curl. -i shows headers, --max-time bounds execution, and no -L means redirects are not followed. Header observations alone do not prove exploitability; this fixture has no sensitive authenticated content.

## ffuf: four reviewed paths

```sh
ffuf -w paths.txt -u http://127.0.0.1:8891/FUZZ -t 1 -rate 1 -timeout 5 -maxtime 15 -mc all
```

-w selects the four-line wordlist, FUZZ is replaced, -t limits concurrency, -rate limits requests per second, -timeout bounds each request and -maxtime bounds the run. -mc all preserves the 404 control. Expect strong=200, weak=200, redirect=302 and missing=404. Do not infer vulnerabilities from their presence. No recursion is requested.

## Gobuster: compare a second discovery client

```sh
gobuster dir -u http://127.0.0.1:8891/ -w paths.txt -t 1 --delay 1s --timeout 5s
```

This uses the same four candidates, one worker and a delay. Gobuster may issue an additional baseline probe. Its usual 404 blacklist omits missing from displayed results. Verify individual responses with curl. Do not run ffuf and Gobuster together and accidentally multiply the planned request rate.

## Burp and ZAP: manual analysis

In Burp, scope the loopback origin, record a request and send it to Repeater. Keep the original tab and compare one changed request. Inspect Location, status, body and identity before following a redirect. For authentication and ownership, use the separate casebook on port 8901 and the API workbook.

In ZAP, use Manual Explore or configure a test client proxy to visit only this fixture. Inspect history and passive alerts. Passive analysis of recorded messages differs from crawling or active scanning; Quick Start automated scanning performs additional requests. Resolve each alert against the feature and response context before reporting it.

## Nuclei: understand a matcher and its negative control

```sh
nuclei -validate -t "$HOME/kali-lab/advanced-web/local-header.yaml"
nuclei -u http://127.0.0.1:8891 -t "$HOME/kali-lab/advanced-web/local-header.yaml" -rl 1 -c 1 -ni -duc
```

The local informational template observes the nosniff header on /strong. -t selects only the reviewed file, -rl and -c bound rate and concurrency, -ni disables Interactsh, and -duc disables update checks. The template does not follow redirects. Match means header observed, not vulnerability confirmed. In a copy of the template, change /strong to /weak and repeat: no nosniff match is expected. If nothing matches, first check the fixture is running.

## Semgrep: source candidate to confirmed data flow

```sh
semgrep scan --config "$HOME/kali-lab/advanced-web/review-eval.yaml" --metrics=off "$HOME/kali-lab/advanced-web/sample_review.py"
```

Read the source without executing it. The teaching rule flags eval. Inspect whether input is untrusted, identify a suitable constrained parser, and test both invalid and valid input after a repair. A pattern finding is not a complete reachability proof. A copy without eval is a matcher negative control, not proof the whole program is secure.

## Tool choice and limits

Use browser developer tools for actual DOM and browser policy; Burp for manual request comparisons; ZAP for recorded-message observations; curl for exact exchanges; ffuf/Gobuster for bounded candidate discovery; Nuclei for reviewed template checks; Semgrep for source patterns; Postman and Python for explicit regressions. sqlmap needs a separately authorized SQLi lab and a specific assessment plan. GraphiQL needs a local GraphQL service and known schema. Version banners, scanner severity and missing headers do not establish business impact by themselves.

Official references: [Burp workflow](https://portswigger.net/burp/documentation/desktop/testing-workflow), [ZAP passive scanner](https://www.zaproxy.org/docs/desktop/addons/passive-scanner/), [ffuf](https://github.com/ffuf/ffuf), [Gobuster](https://github.com/OJ/gobuster), [Nuclei](https://docs.projectdiscovery.io/opensource/nuclei/running), [Semgrep](https://docs.semgrep.dev/running-rules).
