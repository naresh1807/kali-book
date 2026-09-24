PROGRAMMING PRACTICE

These are original synthetic training examples. Python scripts use the standard library. Node examples use built-in modules and ES module .mjs files. Use Python 3.10+ and a supported Node release with node:test (the examples were checked using Python 3.12 and Node 24).

Copy the selected files and sample.jsonl into ~/kali-lab/programming inside Kali using your configured shared folder or normal file transfer. A host drive is not automatically mounted in Kali. Do not copy the .venv directory between Windows and Linux.

Offline projects:
python3 log_summary.py sample.jsonl
node log_summary.mjs sample.jsonl

Rule tests:
python3 py_access_tests.py
node --test js_access_tests.mjs

Local HTTP projects (requires the Chapter 24/Lab 13 server running on 127.0.0.1:8877):
python3 local_headers.py 8877
node local_headers.mjs 8877

The two header tools do not follow redirects, accept remote hosts or establish vulnerability findings. No files execute automatically. Browser snippets are printed only in the handbook; run them only on your local training page.
