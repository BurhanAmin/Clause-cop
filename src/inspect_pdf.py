import pymupdf

PDF_PATH = 'data/mcra_1999.pdf'

doc = pymupdf.open(PDF_PATH)

print('Pages:' , len(doc))
print('Metadata: ', doc.metadata)

print("\n Chars per page:")
page_texts=[]
for i, page in enumerate(doc):
    text = page.get_text("text")
    page_texts.append(text)
    print(f" Page {i+1:>2}: {len(text)}")

for page_no in (1,10):
    print(f"\n ==== RAW PAGE {page_no} (first 1200 chars) ====")
    print(repr(page_texts[page_no - 1][:1200]))

with open("data/raw_text.txt", "w", encoding ="utf-8") as f :
    for i, text in enumerate(page_texts):
        f.write(f"\n\n ---- PAGE{i+1} --- \n")
        f.write(text)

print("\n Wrote data/raw_text.txt")