#!/usr/bin/env python3
"""The gate. Refuse to deploy a site that is already broken.

    python3 scripts/validate_site.py _site

Every check here exists because of a way this particular site can break, not
because it is a generic nice-to-have. The site is a Jekyll page that includes a
README which a scheduled bot rewrites on its own; that gives it three failure
modes a human would not notice quickly:

  * the bot's rewrite removes or mangles the activity markers, so the next
    rewrite has nowhere to write and the section quietly stops updating;
  * the Liquid include fails, and the homepage ships with the literal text
    "{% include_relative README.md %}" on it;
  * a link in the README points at a page that does not exist.

Exit status is 0 if the built site may be published, 1 if it may not.
"""

import re
import sys
import os
import urllib.request
import urllib.error
from html.parser import HTMLParser

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
LIQUID_RE = re.compile(r"\{%|\{\{")
MARKERS = ("<!--START_SECTION:activity-->", "<!--END_SECTION:activity-->")

failures = []
notes = []


def fail(check, detail):
    failures.append((check, detail))
    print(f"  FAIL  {check}\n        {detail}")


def ok(check, detail=""):
    print(f"  ok    {check}" + (f"  ({detail})" if detail else ""))


class LinkFinder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ("a", "link"):
            for k, v in attrs:
                if k == "href" and v:
                    self.links.append(v)
        elif tag in ("img", "script"):
            for k, v in attrs:
                if k == "src" and v:
                    self.links.append(v)


def html_files(root):
    for dirpath, _, names in os.walk(root):
        for n in names:
            if n.endswith(".html"):
                yield os.path.join(dirpath, n)


def base_path_of(url):
    """The path a project site is served under, e.g. /devops-pages-lab.

    A project site is published at user.github.io/<repo>/, so every absolute
    link Jekyll writes carries that prefix. Inside _site the same file sits at
    the root, without it - _site/assets/..., not _site/<repo>/assets/... .
    Resolving an absolute link literally therefore reports the theme's own
    stylesheet as a broken link, which is a false failure on every project
    site in existence.
    """
    if not url:
        return ""
    try:
        from urllib.parse import urlparse
        return urlparse(url).path.rstrip("/")
    except Exception:
        return ""


def main(site):
    print(f"Validating {site}\n")
    self_url = os.environ.get("SITE_BASE_URL", "").rstrip("/")
    base_path = base_path_of(self_url)
    if base_path:
        print(f"  (served under {base_path}/)\n")

    if not os.path.isdir(site):
        fail("built site exists", f"{site} is not a directory - did the build step run?")
        return finish()

    # 1. The markers the bot writes between must still be in the SOURCE readme.
    #    If they are gone, the activity section silently stops updating, and
    #    nothing about the published page looks wrong.
    try:
        readme = open("README.md", encoding="utf-8").read()
        missing = [m for m in MARKERS if m not in readme]
        if missing:
            fail("README activity markers", f"missing from README.md: {', '.join(missing)}")
        else:
            ok("README activity markers")
    except FileNotFoundError:
        fail("README activity markers", "README.md not found at the repository root")

    # 2. A homepage was built at all.
    home = os.path.join(site, "index.html")
    if not os.path.isfile(home):
        fail("homepage built", f"{home} does not exist")
        return finish()
    body = open(home, encoding="utf-8").read()
    ok("homepage built", f"{len(body):,} bytes")

    # 3. The include actually ran. A failed include_relative does not error -
    #    it leaves the Liquid tag on the page as plain text.
    leftovers = sorted({
        m.group(0) for f in html_files(site)
        for m in LIQUID_RE.finditer(open(f, encoding="utf-8", errors="replace").read())
    })
    if leftovers:
        fail("Liquid fully rendered",
             f"unrendered template syntax in the output: {', '.join(leftovers)}")
    else:
        ok("Liquid fully rendered")

    # 4. The README reached the homepage. The markers are HTML comments, so
    #    they survive the markdown conversion and prove the include worked.
    if all(m in body for m in MARKERS):
        ok("README included in homepage")
    else:
        fail("README included in homepage",
             "the activity markers are not in the built index.html, so "
             "{% include_relative README.md %} did not bring the README in")

    # 5. This build stamped its own identity into the site. Without it the
    #    smoke test after deployment has nothing to compare against.
    vpath = os.path.join(site, "version.txt")
    if not os.path.isfile(vpath):
        fail("version stamped", "version.txt is not in the built site")
    else:
        v = open(vpath, encoding="utf-8").read().strip()
        if SHA_RE.match(v):
            ok("version stamped", v[:7])
        else:
            fail("version stamped", f"version.txt does not contain a commit SHA: {v!r}")

    # 6. Internal links resolve to something that was actually built.
    internal_bad, external = [], set()
    for f in html_files(site):
        p = LinkFinder()
        p.feed(open(f, encoding="utf-8", errors="replace").read())
        for href in p.links:
            if href.startswith(("http://", "https://")):
                external.add(href)
                continue
            if href.startswith(("mailto:", "tel:", "#", "data:")):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if target.startswith("/"):
                rel = target
                if base_path and (rel == base_path or rel.startswith(base_path + "/")):
                    rel = rel[len(base_path):]
                cand = os.path.normpath(os.path.join(site, rel.lstrip("/")))
            else:
                cand = os.path.normpath(os.path.join(os.path.dirname(f), target))
            if os.path.isfile(cand) or os.path.isfile(os.path.join(cand, "index.html")) \
                    or os.path.isdir(cand):
                continue
            internal_bad.append((os.path.relpath(f, site), href))
    if internal_bad:
        for f, h in internal_bad:
            fail("internal links resolve", f"{f} links to {h}, which was not built")
    else:
        ok("internal links resolve", f"{len(external)} external, checked below")

    # 7. External links: fail only on a definite 404 or 410. A timeout or a
    #    403 from a site that dislikes CI runners is not evidence that the
    #    link is broken, and a gate that blocks deploys on someone else's
    #    rate limiting would be turned off within a week.
    #
    #    Links back to this site are skipped, and not as a convenience. The
    #    gate runs before the deploy, so the live URL still holds the previous
    #    build - or, on the very first run, nothing at all. Checking it would
    #    make the site a precondition of its own first publication, and the
    #    first deploy could never happen. Whether this build is reachable is a
    #    question for the smoke test, after it has been published.
    if self_url:
        skipped = {u for u in external if u.rstrip("/").startswith(self_url)}
        if skipped:
            external -= skipped
            notes.append(f"{len(skipped)} link(s) to this site itself left to the "
                         f"smoke test, not checked here")

    for url in sorted(external):
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "pages-link-check"})
            urllib.request.urlopen(req, timeout=10)
            ok("external link", url)
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                fail("external link", f"{url} returned HTTP {e.code}")
            else:
                notes.append(f"{url} returned HTTP {e.code} - not treated as broken")
        except Exception as e:
            notes.append(f"{url} could not be reached ({type(e).__name__}) - not treated as broken")

    return finish()


def finish():
    print()
    for n in notes:
        print(f"  note  {n}")
    if failures:
        print(f"\nGATE CLOSED - {len(failures)} check(s) failed. Nothing will be deployed.")
        return 1
    print("\nGate open - the built site may be published.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_site"))
