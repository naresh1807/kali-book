# Digital forensics: local workbook

## Offline evidence lab

Extract the lab ZIP and open examples/forensics. Python 3.10+ with its standard library is enough. Commands below use Kali Bash; Windows can use python instead of python3.

```sh
python3 forensic_lab.py
python3 -m unittest -v test_forensics
```

Expected: notes.txt and events.jsonl match their supplied SHA-256 values; the timeline order is evt-1, evt-2, evt-3; all ten tests pass. The last two events have the same normalized time, so their displayed order preserves source order and makes no causal claim. The program reads only these synthetic fixtures and opens no network connection.

For a negative control, copy the entire lab folder to a new practice folder, change notes.txt in that copy and rerun. Expect mismatch and exit status 1 before timeline analysis. Preserve the original folder. Test cases also reject missing timezone information, duplicate IDs and malformed records. Do not regenerate the manifest to hide an unexpected change.

## Hashes and file triage

```sh
sha256sum notes.txt events.jsonl
file notes.txt events.jsonl
strings -n 6 notes.txt
```

Compare the hash output with manifest.json. File identification and printable strings are observations, not proof of provenance or execution. A hash mismatch requires investigation; a match only compares bytes with the chosen baseline. The baseline itself must be preserved and trusted for a real investigation.

For a separately supplied copied photograph, a read-only metadata example is:

```sh
exiftool -a -G1 -s copied-photo.jpg
```

The photograph is not bundled. -a shows duplicate tags, -G1 groups tag output and -s uses tag names. No metadata-writing assignments are included. Preserve original and interpreted timestamp values; embedded metadata can be edited or inherited.

## Autopsy: graphical artifact review

Create a new case in a separate analysis location, record examiner/case identifiers, then add an authorized image or copied logical source. Select only ingest modules relevant to the question and record their versions and settings. Review parser errors, inspect source artifacts behind findings and export selected results separately from evidence.

For this small fixture, a logical-files import can help you practice case organization; it does not create a disk image or demonstrate deleted-file recovery. Keyword hits and timeline entries need interpretation. Recheck important conclusions against original fields and, where practical, another parser.

## Sleuth Kit: disk-image prerequisites

These commands require a separately obtained authorized compatible disk image named lab-disk.img. No image is bundled. Work on a verified copy and create a separate analysis directory before exporting artifacts.

```sh
mmls lab-disk.img
```

Identify the intended partition and its starting sector from this image. Confirm the sector size and whether the input is a whole disk or a file-system image. In the next commands, START_SECTOR must already contain the verified numeric sector offset and METADATA_ADDRESS the selected record identifier from fls; neither value is supplied or guessed by the book.

```sh
fsstat -o "$START_SECTOR" lab-disk.img
fls -r -o "$START_SECTOR" lab-disk.img
icat -o "$START_SECTOR" lab-disk.img "$METADATA_ADDRESS" > analysis/recovered.bin
sha256sum analysis/recovered.bin
```

Use a new output name to preserve earlier exports. fls lists names/metadata; icat exports the selected record content. Units matter: -o is an image offset in sectors, not a byte count. A parser failure calls for checking layout, format and support before declaring corruption. Treat recovered content as untrusted and do not execute it.

## Volatility 3: memory-image prerequisites

This requires a separately acquired authorized memory image, a working Volatility 3 source checkout and matching symbol support. From that checkout, after locating the copied dump:

```sh
python3 vol.py -f memory.raw windows.info
python3 vol.py -f memory.raw windows.pslist
```

These are Windows-image examples; use the appropriate plugins for another operating system. Check installed help because plugin naming and requirements vary by version. Symbol setup may download files, so plan it within the analysis environment's network policy. Record errors and symbol provenance. A process list is a starting observation, not proof that a named process is malicious. No dump, live acquisition or credential extraction is included in this workbook.

## Saved network captures

Use only an authorized saved capture, such as the synthetic local.pcap created in the network workbook. It is not bundled with this folder.

```sh
tshark -r local.pcap -Y 'tcp' -T fields -e frame.number -e frame.time_epoch -e ip.src -e ip.dst -e tcp.len
```

Open the same file in Wireshark, examine packet details and follow the relevant stream. A display filter does not remove packets from the source file. Record capture location, missing directions, packet loss and whether payloads are encrypted. A source address alone cannot establish a person's identity. Use the original capture timestamp values when correlating with host events.

## Timeline interpretation and broader tools

The supplied Python lab converts explicit ISO timestamps to UTC, keeps original fields and refuses timezone-naive records. It does not correct clock skew or parse binary operating-system logs. Its synthetic manifest authenticates neither origin nor historical integrity.

For larger datasets, Plaso can extract temporal artifacts and Timesketch can support exploration. Their parser selection, source coverage and timezone assumptions need validation. ExifTool metadata, browser records and file-system times can refer to different events. YARA matches locally reviewed rules; matches are leads, not automatic verdicts. PhotoRec carves recognizable content but may not reconstruct original paths or times.

## Evidence worksheet and report

Case identifier:
Investigative question and authorized sources:
Evidence item/source description:
Acquisition method, tool/version, start/end time and effects:
SHA-256 baseline and verification events:
Custody transfer: from, to, time, reason, storage and access controls:
Working-copy identifier and derived outputs:
Original timestamps, timezone assumptions and normalized values:
Observed artifact and location:
Interpretation and alternative explanations:
Confidence, missing evidence and parser limitations:
Independent validation and final integrity check:

Keep conclusions narrower than evidence. Use synthetic or redacted details in shared reports and store sensitive source artifacts separately.

References: [Sleuth Kit fls](https://www.sleuthkit.org/sleuthkit/man/fls.html), [Sleuth Kit tools](https://www.sleuthkit.org/sleuthkit/man/), [Autopsy](https://www.autopsy.com/), [Volatility 3](https://volatility3.readthedocs.io/en/latest/), [Wireshark](https://www.wireshark.org/docs/wsug_html_chunked/).
