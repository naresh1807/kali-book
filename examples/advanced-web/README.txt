ADVANCED WEB TOOL EXERCISES

Copy this folder into ~/kali-lab/advanced-web in Kali. See chapters 32–33 and Lab 18. Tools must be installed separately using their official documentation.

Nuclei: inspect local-header.yaml, validate it, then use the local fixture from Chapter 30. This template observes a header, not a vulnerability.
Semgrep: inspect review-eval.yaml and scan sample_review.py. The sample function is deliberately unsafe teaching material; do not execute it or reuse it in an application.
Arjun: parameters.txt is a three-word training list. The local fixture ignores these parameters, so it provides a negative control.

No scanner runs automatically. Reports may contain sensitive evidence even when secrets are redacted.
