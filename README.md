# Clause Cop

> Point at a rental agreement, see the risky clauses highlighted on the page, with the law that backs it up.

Clause Cop takes a rental agreement (PDF or photo), splits it into clauses, checks each clause against relevant tenancy law using Retrieval-Augmented Generation (RAG), and overlays **red / amber / green** highlights on the original page. Click a highlight to see a one-line reason and the exact statute it was matched against.

**Not legal advice.** Clause Cop is a learning project. Its output can be wrong. Always verify against the cited source and consult a qualified lawyer for real decisions.

---

## Why this project exists

The app is secondary. The real goal is to learn, end to end:

1. How RAG systems work, from basic to advanced.
2. How to deploy a RAG system.
3. How to diagnose and fix problems inside a RAG system (bad retrieval, poor chunking, hallucinated citations, false flags, latency).

Every design decision in this repo is documented with the reasoning behind it, not just the result.

---

## How it works

```
Contract (PDF / photo)
        │
        ▼
  OCR / vision  ──►  clause splitting  ──►  per-clause query
                                                  │
                                                  ▼
Legal corpus ──► chunk ──► embed ──► vector store ──► retrieve (+ rerank)
                                                  │
                                                  ▼
                                   LLM classifies clause
                              (standard / unusual / likely unenforceable)
                                                  │
                                                  ▼
                                    verification pass (drop weak flags)
                                                  │
                                                  ▼
                           page overlay: colored highlights + citations
```

Key idea: retrieval happens **per clause**, not per document, so each clause is compared against the most relevant provisions.

---

## Scope

- Rental agreements only
- One state
- English documents
- Legal corpus: Model Tenancy Act plus the chosen state's rent law

Out of scope for now: loans, employment contracts, other languages, multi-state support.

---

## Build roadmap

- [ ] **Level 1: Basic RAG.** Ingest legal text, chunk, embed, store, retrieve, answer questions with citations.
- [ ] **Level 2: Clause-by-clause analysis.** Split a contract into clauses, retrieve per clause, return structured output.
- [ ] **Level 3: Visual overlay.** OCR or vision model for clause bounding boxes, draw highlights, link each one to its retrieved law.
- [ ] **Level 4: Advanced.** Routing (which law applies), self-verification of flags, evaluation on real agreements.
- [ ] **Deployment.** Hosting, persistent vector store, API key handling, cost and latency, monitoring.

---

## Tech stack

| Layer | Choice |
|---|---|
| Language | Python |
| Vector store | Chroma |
| Embeddings | Embeddings API (or sentence-transformers) |
| LLM | Vision-capable LLM |
| UI | Streamlit (or Next.js for the overlay UI) |

Final choices and the tradeoffs behind them are recorded in `docs/decisions.md`.

---

## Suggested project structure

```
clause-cop/
├── data/
│   ├── legal/            # source statutes (PDF/text)
│   ├── contracts/        # sample agreements for testing
│   └── eval/             # labeled test set
├── src/
│   ├── ingest.py         # load, chunk, embed, store legal text
│   ├── retrieve.py       # retrieval (and reranking)
│   ├── clauses.py        # contract parsing and clause splitting
│   ├── analyze.py        # per-clause classification + verification
│   ├── overlay.py        # bounding boxes and highlight rendering
│   └── eval.py           # evaluation harness
├── app.py                # UI entry point
├── docs/
│   └── decisions.md      # design decisions and what I learned
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Clone and enter the repo
git clone <your-repo-url>
cd clause-cop

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# then edit .env and add your keys
```

Environment variables (names may change as the project evolves):

```
EMBEDDING_API_KEY=
LLM_API_KEY=
```

---

## Usage

```bash
# Build the vector store from the legal corpus
python src/ingest.py

# Launch the app
streamlit run app.py
```

Then upload a rental agreement and review the highlighted clauses.

---

## Evaluation

RAG quality is measured, not guessed. The evaluation set lives in `data/eval/` and tracks two things separately:

- **Retrieval quality:** did the right legal provision show up in the top-k results?
- **Answer quality:** was the clause classified correctly, and was the citation accurate?

Every change (chunk size, reranker, prompt, model) should be compared against the same test set before it is kept. A false-flag rate is tracked specifically, since wrongly flagging a fair clause is the main failure mode.

---

## Known limitations

- May miss risky clauses or flag fair ones (false negatives and false positives).
- Depends on OCR quality for photos and scanned pages.
- Covers only the configured state's law and the Model Tenancy Act.
- Laws change; the corpus must be kept up to date manually.
- Citations must be checked against the original text.

---

## What I'm learning

Notes on chunking, retrieval failures, debugging methods, and deployment decisions are kept in `docs/decisions.md`, updated at each milestone.

---

## License

Choose a license (e.g. MIT) before publishing.