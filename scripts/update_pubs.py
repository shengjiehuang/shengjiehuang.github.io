#!/usr/bin/env python3
"""Rebuild _bibliography/papers.bib from arXiv.

Data sources (see scripts/publications.json):
  * arxiv_author_id  -- your arXiv author feed (arxiv.org/a/<id>); preferred once you
                        have claimed your papers on arXiv.
  * search_query     -- arXiv API search used when no author id is set.
  * extra_arxiv_ids  -- papers the feed/search misses (e.g. listed under another name form).
  * exclude_arxiv_ids-- papers to leave out (e.g. by a namesake).

Hand corrections live in _bibliography/manual.bib:
  * an entry with  arxiv = {XXXX.XXXXX}  overrides those fields of the automatic entry;
  * an entry with  arxiv = {...}, skip = {true}  removes that paper;
  * any other entry is added as-is (for papers that are not on arXiv).

Standard library only. Usage:  python3 scripts/update_pubs.py
"""

import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "scripts" / "publications.json"
MANUAL = ROOT / "_bibliography" / "manual.bib"
OUTPUT = ROOT / "_bibliography" / "papers.bib"

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
USER_AGENT = "al-folio-publication-updater/1.0 (personal academic website)"

# Short labels shown as badges next to each paper.
ABBR = [
    (r"^Phys\.? ?Rev\.? ?Lett", "PRL"),
    (r"^Phys\.? ?Rev\.? ?X", "PRX"),
    (r"^Phys\.? ?Rev\.? ?Research", "PRR"),
    (r"^Phys\.? ?Rev\.? ?B|^Physical Review B", "PRB"),
    (r"^Phys\.? ?Rev\.? ?A|^Physical Review A", "PRA"),
    (r"^PRX Quantum", "PRX Quantum"),
    (r"^SciPost", "SciPost"),
    (r"^npj Quantum Mater", "npj QM"),
    (r"^Sci\.? ?Adv", "Sci. Adv."),
    (r"^Nat(ure)?\.? ?Phys", "Nat. Phys."),
    (r"^Nat(ure)?\.? ?Commun", "Nat. Commun."),
    (r"^Quantum\b", "Quantum"),
]

FIELD_ORDER = [
    "abbr", "bibtex_show", "title", "author", "journal", "volume", "pages", "year",
    "doi", "html", "arxiv", "annotation", "award", "award_name",
    "selected", "pdf", "slides", "video", "code", "abstract",
]


# ----------------------------------------------------------------------------- fetching

def fetch(url: str, retries: int = 4) -> bytes:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as exc:  # network hiccup or arXiv rate limit
            if attempt == retries - 1:
                raise
            wait = 5 * (attempt + 1)
            print(f"  fetch failed ({exc}); retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def ids_from_atom(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    ids = []
    for entry in root.findall("a:entry", NS):
        raw = entry.findtext("a:id", default="", namespaces=NS)
        if "/abs/" in raw:
            ids.append(strip_version(raw.split("/abs/")[-1]))
    return ids


def strip_version(arxiv_id: str) -> str:
    return re.sub(r"v\d+$", "", arxiv_id.strip())


def collect_ids(cfg: dict) -> list[str]:
    ids: list[str] = []
    author_id = (cfg.get("arxiv_author_id") or "").strip()
    if author_id:
        print(f"Reading arXiv author feed {author_id}")
        ids += ids_from_atom(fetch(f"https://arxiv.org/a/{urllib.parse.quote(author_id)}.atom2"))
    else:
        query = cfg["search_query"]
        print(f"Searching arXiv for {query}")
        params = urllib.parse.urlencode({"search_query": query, "max_results": 500})
        ids += ids_from_atom(fetch(f"{API}?{params}"))
    ids += [strip_version(i) for i in cfg.get("extra_arxiv_ids", [])]
    excluded = {strip_version(i) for i in cfg.get("exclude_arxiv_ids", [])}
    seen, result = set(), []
    for i in ids:
        if i not in seen and i not in excluded:
            seen.add(i)
            result.append(i)
    if not result:
        sys.exit("No arXiv papers found; refusing to overwrite papers.bib")
    return result


def fetch_metadata(ids: list[str]) -> list[dict]:
    papers = []
    for start in range(0, len(ids), 50):
        chunk = ids[start:start + 50]
        if start:
            time.sleep(3)  # arXiv asks for at most one request every 3 seconds
        params = urllib.parse.urlencode({"id_list": ",".join(chunk), "max_results": len(chunk)})
        root = ET.fromstring(fetch(f"{API}?{params}"))
        for e in root.findall("a:entry", NS):
            raw_id = e.findtext("a:id", default="", namespaces=NS)
            if "/abs/" not in raw_id:
                continue  # error entry
            papers.append({
                "arxiv": strip_version(raw_id.split("/abs/")[-1]),
                "title": clean(e.findtext("a:title", default="", namespaces=NS)),
                "abstract": clean(e.findtext("a:summary", default="", namespaces=NS)),
                "authors": [clean(a.findtext("a:name", default="", namespaces=NS)) for a in e.findall("a:author", NS)],
                "published": e.findtext("a:published", default="", namespaces=NS),
                "journal_ref": clean(e.findtext("x:journal_ref", default="", namespaces=NS)),
                "doi": clean(e.findtext("x:doi", default="", namespaces=NS)).split()[0] if e.findtext("x:doi", default="", namespaces=NS) else "",
            })
    found = {p["arxiv"] for p in papers}
    missing = [i for i in ids if i not in found]
    if missing:
        print(f"  warning: arXiv returned nothing for {', '.join(missing)}", file=sys.stderr)
    return papers


def clean(text: str) -> str:
    return " ".join((text or "").split())


# ----------------------------------------------------------------------------- converting

def bib_name(name: str) -> str:
    """'Sheng-Jie Huang' -> 'Huang, Sheng-Jie';  'S. -J. Huang' -> 'Huang, S.-J.'"""
    name = re.sub(r"\.\s+-", ".-", name)
    parts = name.split()
    if len(parts) < 2:
        return name
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def parse_journal_ref(ref: str) -> dict:
    """'Phys. Rev. B 105, 094518 (2022)' -> journal, volume, pages, year."""
    m = re.match(r"^(?P<journal>.*?\D)\s*(?P<volume>\d+)\s*(?:\(\d+\))?\s*[,:]\s*(?P<pages>[\w.-]+)\s*,?\s*\(?(?P<year>(?:19|20)\d\d)\)?", ref)
    if not m:
        y = re.search(r"(19|20)\d\d", ref)
        return {"journal": ref, "year": y.group(0) if y else ""}
    return {k: v.strip().rstrip(",") for k, v in m.groupdict().items()}


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", text.lower())


STOPWORDS = {"a", "an", "the", "on", "of", "in", "for", "and", "with", "to", "via", "from", "beyond", "through"}


def make_key(paper: dict) -> str:
    first_last = slug(bib_name(paper["authors"][0]).split(",")[0]) if paper["authors"] else "anon"
    year = paper["published"][:4]
    words = [slug(w) for w in re.sub(r"\$[^$]*\$", " ", paper["title"]).split()]
    word = next((w for w in words if w and w not in STOPWORDS), "paper")
    return f"{first_last}{year}{word}"


def to_entry(paper: dict) -> dict:
    fields: dict[str, str] = {
        "bibtex_show": "true",
        "title": paper["title"],
        "author": " and ".join(bib_name(a) for a in paper["authors"]),
        "arxiv": paper["arxiv"],
        "abstract": paper["abstract"],
    }
    if paper["journal_ref"]:
        ref = parse_journal_ref(paper["journal_ref"])
        fields["journal"] = ref["journal"]
        fields["year"] = ref.get("year") or paper["published"][:4]
        if ref.get("volume"):
            fields["volume"] = ref["volume"]
            fields["pages"] = ref["pages"]
    else:
        fields["journal"] = f"arXiv:{paper['arxiv']}"  # shown as e.g. "arXiv:2610.27556, 2026"
        fields["year"] = paper["published"][:4]
    if paper["doi"]:
        fields["doi"] = paper["doi"]
    return {"type": "article", "key": make_key(paper), "fields": fields, "sort": paper["published"]}


def finalize(entry: dict) -> dict:
    """Fill in display-only fields from the (possibly overridden) bibliographic ones."""
    f = entry["fields"]
    if "abbr" not in f:
        journal = f.get("journal", "")
        f["abbr"] = next((label for pattern, label in ABBR if re.search(pattern, journal)), "arXiv" if journal.startswith("arXiv:") else "")
        if not f["abbr"]:
            del f["abbr"]
    return entry


# ----------------------------------------------------------------------------- BibTeX I/O

def parse_bib(text: str) -> list[dict]:
    """Minimal BibTeX parser: @type{key, field = {value} | "value" | number, ...}."""
    entries, i = [], 0
    while (at := text.find("@", i)) != -1:
        brace = text.find("{", at)
        if brace == -1:
            break
        etype = text[at + 1:brace].strip().lower()
        depth, j = 1, brace + 1
        while j < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        body = text[brace + 1:j - 1]
        i = j
        if etype in ("comment", "string", "preamble"):
            continue
        key, _, rest = body.partition(",")
        fields, k = {}, 0
        while (m := re.compile(r"\s*([\w-]+)\s*=\s*").match(rest, k)):
            name, k = m.group(1).lower(), m.end()
            if rest[k] == "{":
                depth, start = 1, k + 1
                k += 1
                while depth:
                    depth += {"{": 1, "}": -1}.get(rest[k], 0)
                    k += 1
                value = rest[start:k - 1]
            elif rest[k] == '"':
                end = rest.index('"', k + 1)
                value, k = rest[k + 1:end], end + 1
            else:
                vm = re.compile(r"[^,\s]+").match(rest, k)
                value, k = vm.group(0), vm.end()
            fields[name] = clean(value)
            k = rest.find(",", k) + 1 if rest.find(",", k) != -1 else len(rest)
        entries.append({"type": etype, "key": key.strip(), "fields": fields})
    return entries


def format_entry(entry: dict) -> str:
    f = entry["fields"]
    names = [n for n in FIELD_ORDER if n in f] + sorted(n for n in f if n not in FIELD_ORDER)
    width = max(len(n) for n in names)
    lines = [f"@{entry['type']}{{{entry['key']},"]
    lines += [f"  {n.ljust(width)} = {{{f[n]}}}," for n in names]
    lines[-1] = lines[-1].rstrip(",")
    return "\n".join(lines) + "\n}\n"


# ----------------------------------------------------------------------------- main

def main() -> None:
    cfg = json.loads(CONFIG.read_text())
    papers = fetch_metadata(collect_ids(cfg))
    entries = {p["arxiv"]: to_entry(p) for p in papers}

    manual = parse_bib(MANUAL.read_text()) if MANUAL.exists() else []
    extra = []
    for m in manual:
        target = strip_version(m["fields"].get("arxiv", ""))
        if target and target in entries:
            if m["fields"].get("skip", "").lower() == "true":
                del entries[target]
                continue
            entries[target]["fields"].update({k: v for k, v in m["fields"].items() if k != "skip"})
        elif target:
            print(f"  note: manual.bib override for {target} matches no arXiv paper; adding it as its own entry", file=sys.stderr)
            extra.append({**m, "sort": m["fields"].get("year", "0000")})
        else:
            extra.append({**m, "sort": m["fields"].get("year", "0000")})

    all_entries = [finalize(e) for e in list(entries.values()) + extra]
    used: set[str] = set()
    for e in sorted(all_entries, key=lambda e: e["fields"].get("arxiv", e["key"])):
        base, n = e["key"], 1
        while e["key"] in used:  # same first author, year and first title word
            n += 1
            e["key"] = f"{base}{n}"
        used.add(e["key"])
    # Newest first; jekyll-scholar groups by year but keeps this order inside a year.
    all_entries.sort(key=lambda e: (e["fields"].get("year", "0000"), e["sort"]), reverse=True)

    out = "---\n---\n\n% Generated by scripts/update_pubs.py from arXiv -- do not edit by hand.\n% Put corrections in _bibliography/manual.bib instead.\n\n"
    out += "\n".join(format_entry(e) for e in all_entries)
    if OUTPUT.exists() and OUTPUT.read_text() == out:
        print(f"No changes ({len(all_entries)} papers).")
        return
    OUTPUT.write_text(out)
    print(f"Wrote {len(all_entries)} papers to {OUTPUT.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
