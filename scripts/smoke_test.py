#!/usr/bin/env python3
"""The smoke test. Confirm the live site is serving THIS build.

    python3 scripts/smoke_test.py https://user.github.io/repo/ <commit-sha>

A deploy can report success and leave the old site in place: the CDN can serve
a cached copy, the artifact can be stale, a concurrent run can win the race. In
every one of those cases the site answers HTTP 200, so a status-code check
passes while the change the deploy was for is not actually live.

The only way to tell is to ask the live site which build it is. Every build
writes its own commit SHA into version.txt, so that question has an answer, and
this script fails the workflow unless the answer is the SHA just deployed.

Pages serves through a CDN, so the first few requests after a deploy can still
return the previous build. That is propagation, not failure, so the check is
retried before it gives up - but it gives up.
"""

import os
import sys
import time
import urllib.request
import urllib.error

# Up to two minutes of CDN propagation by default. Overridable so the same
# script can be exercised quickly in a test without editing it, which is the
# only way a check like this ever gets tested at all.
ATTEMPTS = int(os.environ.get("SMOKE_ATTEMPTS", "12"))
INTERVAL = float(os.environ.get("SMOKE_INTERVAL", "10"))


def get(url, timeout=15):
    req = urllib.request.Request(
        url, headers={"User-Agent": "pages-smoke-test", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def main(base, expected):
    base = base.rstrip("/") + "/"
    expected = expected.strip()
    version_url = base + "version.txt"

    print(f"Live site : {base}")
    print(f"Expecting : {expected[:7]}  ({expected})\n")

    served = None
    for attempt in range(1, ATTEMPTS + 1):
        try:
            status, body = get(version_url)
            served = body.strip()
            if served == expected:
                print(f"  attempt {attempt:>2}: serving {served[:7]}  <- match")
                break
            print(f"  attempt {attempt:>2}: serving {served[:7] or '(empty)'}  "
                  f"- not this build yet")
        except urllib.error.HTTPError as e:
            print(f"  attempt {attempt:>2}: HTTP {e.code} for version.txt")
            served = f"HTTP {e.code}"
        except Exception as e:
            print(f"  attempt {attempt:>2}: {type(e).__name__} - {e}")
            served = f"{type(e).__name__}"
        if attempt < ATTEMPTS:
            time.sleep(INTERVAL)
    else:
        print(f"\nSMOKE TEST FAILED after {ATTEMPTS} attempts "
              f"({ATTEMPTS * INTERVAL:.0f}s).")
        print(f"  expected : {expected}")
        print(f"  serving  : {served}")
        print("\nThe deploy reported success and the site is up, but it is not "
              "this build.\nRun rollback.yml against the last known-good "
              "release rather than\nredeploying the same commit and hoping.")
        return 1

    # The version matched, so this IS the right build. Now check the build is
    # not merely present but usable: the homepage has to carry the README that
    # the whole site exists to publish.
    print()
    try:
        status, home = get(base)
    except Exception as e:
        print(f"  FAIL  homepage: {type(e).__name__} - {e}")
        return 1
    print(f"  ok    homepage returns HTTP {status}")

    problems = []
    if "<!--START_SECTION:activity-->" not in home:
        problems.append("the activity markers are missing - the README was not included")
    if "{%" in home or "{{" in home:
        problems.append("unrendered Liquid is on the live page")
    if len(home) < 500:
        problems.append(f"the homepage is only {len(home)} bytes - it looks empty")

    for p in problems:
        print(f"  FAIL  {p}")
    if problems:
        print("\nSMOKE TEST FAILED - the right version is live, but it is broken.")
        return 1

    print("  ok    activity section present")
    print("  ok    no unrendered template syntax")
    print(f"\nSmoke test passed - {expected[:7]} is live and serving the README.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: smoke_test.py <base-url> <expected-sha>")
    sys.exit(main(sys.argv[1], sys.argv[2]))
