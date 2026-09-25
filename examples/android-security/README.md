# Android security workbook

## 1. Assessment setup

Use an Android Studio emulator and your own debug APK with synthetic data. No APK is supplied here. Record API level, target SDK, app build and authorized backend scope. Create a baseline snapshot before changing state. Rooting and bootloader unlocking are not prerequisites. Emulation does not fully model physical hardware security.

## 2. ADB commands and their meaning

Install Android SDK Platform Tools and start your emulator. Select its serial from adb devices -l. Replace emulator-5554 with your test emulator serial and org.example.training with your own demo package. The commands inspect the chosen target; the website does not run them.

```sh
adb version
adb devices -l
adb -s emulator-5554 shell getprop ro.build.version.sdk
adb -s emulator-5554 shell dumpsys package org.example.training
adb -s emulator-5554 shell pm path org.example.training
adb -s emulator-5554 shell run-as org.example.training ls files
```

version reports the client version. devices -l lists targets and authorization state. getprop reads the platform API level. dumpsys package reports metadata and permission state: a requested permission is not necessarily granted. pm path prints installed APK paths, including splits when present. run-as runs under a compatible debuggable package identity; release packages generally reject it, and files may not yet exist. Do not interpret either error as proof of an app vulnerability.

With optional tools installed, jadx-gui training.apk opens your own APK for code review. apktool d training.apk -o decoded-training decodes into a new output folder; choose one that does not contain existing work. Record tool versions and preserve the original APK.

## 3. Choose the right tool

Android Studio supplies the emulator, APK Analyzer, debugger and profiler. Start with a repeatable test and recorded baseline.

JADX and Apktool support static review. Reconstructed code may differ from source; verify behavior before reporting impact.

MobSF organizes automated findings. Review an owned APK locally and validate warnings; do not upload private builds to unapproved services.

Burp Suite and mitmproxy inspect synthetic traffic with a deliberate debug trust configuration. Capture only the scoped app and test accounts. Restore proxy and CA settings afterward.

Frida supports runtime observation of a permitted training process. Record how instrumentation changes the environment. Logcat can reveal accidental logging of fake secrets; filter to the training app and redact identifiers.

## 4. Practice cases with expected results

Permission denied: deny an optional permission in the demo app. Expected: safe fallback without a crash or unauthorized access.

Account boundary: create a note as test account A and request it as B on your owned staging API. Expected: rejection with no note contents. Remove synthetic data afterward.

Storage lifecycle: save a dummy session, sign out and inspect permitted debug app storage. Expected: cleanup consistent with policy. Separately verify backend revocation.

Untrusted link: send a harmless malformed link through the app test harness. Expected: safe error and no privileged operation.

Release review: compare debug and release merged manifests and network configuration. Expected: no accidental debugging, test CA trust or unnecessary exported component.

## 5. Finding and retest template

Title and affected build:
Scope and prerequisites:
OS/API level and target SDK:
Expected and observed behavior:
Minimal reproduction with synthetic data:
Evidence and redactions:
Impact and confidence:
Root cause and remediation:
Negative-case retest:
Valid-use regression test:
Coverage limits and cleanup:

## 6. Primary references

[OWASP MASVS](https://mas.owasp.org/MASVS/)
[MASTG techniques](https://mas.owasp.org/MASTG/techniques/)
[ADB documentation](https://developer.android.com/tools/adb)
[Android security guidance](https://developer.android.com/privacy-and-security/security-best-practices)
[Android Keystore](https://developer.android.com/privacy-and-security/keystore)
[Network Security Configuration](https://developer.android.com/privacy-and-security/security-config)
[JADX](https://github.com/skylot/jadx)
[Apktool](https://apktool.org/docs/)
[MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF)
[Frida Android documentation](https://frida.re/docs/android/)

Check platform-version notes before applying a test. This workbook provides manual exercises, not a supplied app or a completed device assessment.


## 7. Advanced assessment matrix

For lessons 19-30, record a separate row for each case: boundary, starting state, synthetic input, expected outcome, observed outcome, confidence, remediation and retest.

IPC: compare a permitted caller with an unapproved caller. Confirm the sensitive operation itself checks authorization.

Provider: compare permitted sharing with an out-of-scope fixture identifier. Confirm no unrelated rows or files are returned.

Session: compare ordinary sign-in, invalid callback correlation, logout and account switching. Inspect both client and staging-server evidence.

WebView: compare approved origin, unexpected origin and redirected navigation. A bridge must not gain authority merely because a page loaded.

TLS: compare valid endpoint, invalid trust and offline failure. Verify that release settings preserve certificate validation.

Native parser: compare valid fixture and bounded malformed fixture under an available sanitizer build. Save a minimal reproducer without inferring exploitability from a crash alone.

Radio interfaces: use only owned paired peers. Check consent, identity and revocation rather than attempting nearby-device takeover.

## 8. Advanced references and practice limits

[Android security risks](https://developer.android.com/privacy-and-security/risks)
[MASTG Android testing](https://mas.owasp.org/MASTG/0x05b-Android-Security-Testing/)
[MASTG testing techniques](https://mas.owasp.org/MASTG/techniques/)
[Intent and component concepts](https://developer.android.com/guide/components/intents-filters)
[PendingIntent sender identity](https://developer.android.com/privacy-and-security/risks/sender-of-pending-intents)

These are manual practice plans for owned test applications, synthetic data and controlled peers. No Android binary, mobile exploit or completed device assessment is included. Record OS/API level and target SDK because platform behavior changes across versions.
