import re
import json 
import pymupdf

doc = pymupdf.open('data/mcra_1999.pdf')

lines = []
for i, page in enumerate(doc):
    for ln in page.get_text("text").splitlines():
        if ln.strip():
            lines.append((i+1, ln.strip()))

pattern = re.compile(r"^\s*\d+[A-Z]?\s*[.\-–—]")

starts = []
expected = 1
for idx, (page_no, ln) in enumerate(lines):
    m = pattern.match(ln)
    if m and int(m.group(1))==expected:
        starts.append((page_no,ln))
        expected +=1
print("Section found: ", len(starts))
