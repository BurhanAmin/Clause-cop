import re
import json
import pymupdf

doc = pymupdf.open("data/mcra_1999.pdf")

# Flatten the PDF to (page, line) pairs so we never lose page numbers
lines = []
for i, page in enumerate(doc):
    for ln in page.get_text("text").splitlines():
        if ln.strip():
            lines.append((i + 1, ln.strip()))

pattern = re.compile(r"^(\d+)\s*[.\-–—]")

# A line starts section N only if N is exactly the next expected number
starts = []
expected = 1
for idx, (page_no, ln) in enumerate(lines):
    m = pattern.match(ln)
    if m and int(m.group(1)) == expected:
        starts.append((expected, idx))
        expected += 1

print("Sections found:", len(starts))

# Preamble = everything before section 1 (title page content)
print("\n--- PREAMBLE ---")
for page_no, ln in lines[: starts[0][1]]:
    print(f"p{page_no}: {ln}")

# Build section records
sections = []
for k, (num, start_idx) in enumerate(starts):
    end_idx = starts[k + 1][1] if k + 1 < len(starts) else len(lines)
    chunk_lines = lines[start_idx:end_idx]
    sections.append({
        "section": num,
        "heading": chunk_lines[0][1],
        "page_start": chunk_lines[0][0],
        "page_end": chunk_lines[-1][0],
        "text": "\n".join(ln for _, ln in chunk_lines),
    })

# Length stats: shortest and longest by word count
by_len = sorted(sections, key=lambda s: len(s["text"].split()))
print("\nShortest 5:")
for s in by_len[:5]:
    print(f"  s{s['section']:>2}: {len(s['text'].split()):>5} words")
print("Longest 5:")
for s in by_len[-5:]:
    print(f"  s{s['section']:>2}: {len(s['text'].split()):>5} words")

# Chapter headings get glued onto the END of the previous section
print("\nChapter-like lines and which section swallowed them:")
for s in sections:
    for ln in s["text"].splitlines():
        if ln.upper().startswith("CHAPTER"):
            print(f"  inside s{s['section']}: {ln!r}")

with open("data/sections.json", "w", encoding="utf-8") as f:
    json.dump(sections, f, ensure_ascii=False, indent=2)
print("\nWrote data/sections.json")