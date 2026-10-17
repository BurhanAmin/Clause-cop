import re
from collections import Counter
import pymupdf

doc = pymupdf.open('data/mcra_1999.pdf')
pages = [p.get_text("text") for p in doc]

line_counts = Counter()
for text in pages:
    unique_lines = {ln.strip() for ln in text.splitlines() if ln.strip()}
    line_counts.update(unique_lines)

print("Lines appearing on 5+ pages: ")
for line, n in line_counts.most_common(15):
    if n>=5:
        print(f" {n:>2} pages: {line!r}")

# 2. First 3 and last 3 lines of a few pages, to see headers directly
for page_no in (3, 12, 25):
    lines = [ln for ln in pages[page_no - 1].splitlines() if ln.strip()]
    print(f"\nPage {page_no} top:    {lines[:3]!r}")
    print(f"Page {page_no} bottom: {lines[-3:]!r}")

# 3. Lines that look like section starts, e.g. "15." or "15A." or "15 -"
pattern = re.compile(r"^\s*\d+[A-Z]?\s*[.\-–—]")
print("\nLines that look like section starts:")
for i, text in enumerate(pages):
    for ln in text.splitlines():
        if pattern.match(ln):
            print(f"  p{i + 1:>2}: {ln!r}")