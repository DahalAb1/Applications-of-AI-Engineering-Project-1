# The Unofficial Guide — Project 1

---

## Domain

This RAG system covers undergraduate STEM scholarships — eligibility criteria, award amounts, deadlines, and application requirements across federal, institutional, and private programs. The knowledge is hard to find in one place because opportunities are scattered across hundreds of individual program websites, government portals, and nonprofit pages, with no single authoritative source that aggregates them. Students who don't know the right organizations to search often miss scholarships they qualify for entirely.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Goldwater Scholarship | Website | https://goldwaterscholarship.gov |
| 2 | Opportunity Desk | Website | https://opportunitydesk.org |
| 3 | College Board Trends in Student Aid 2025 | PDF | documents/collegeboard_trends_student_aid_2025.pdf |
| 4 | Sallie Mae — How America Pays for College 2025 | PDF | documents/salliemae_how_america_pays_2025.pdf |
| 5 | NCSES STEM Talent: Education, Training & Workforce | PDF | documents/ncses_stem_talent_indicators.pdf |
| 6 | NCSES Survey of Doctorate Recipients 2023 | PDF | documents/ncses_stem_workforce_survey_2023.pdf |
| 7 | Lumina Foundation — Some College, No Credential 2025 | PDF | documents/lumina_some_college_no_credential_2025.pdf |
| 8 | NCSES Federal R&D Funding FY 2024–25 | PDF | documents/ncses_federal_rd_funding_2025.pdf |
| 9 | NCES Trends in Graduate Degrees by Field 2024 | PDF | documents/nces_stem_enrollment_trends.pdf |
| 10 | CRA Taulbee Survey 2022–2023 | PDF | documents/cra_taulbee_survey_2023.pdf |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** My documents are dense policy and statistical reports where one paragraph typically covers one complete idea. Pinecone's chunking documentation recommends 256–512 tokens as the starting range for most document types, with longer chunks suited to dense, structured text. 500 characters captures a full paragraph without blending adjacent topics. The 50-character overlap follows the commonly cited 10% rule, which is enough to catch facts that straddle chunk boundaries without duplicating so much content that adjacent chunks become redundant. One known limitation: all-MiniLM-L6-v2 has a 256-token input ceiling, so very long chunks get truncated before embedding. In practice, the opening sentences of a paragraph typically establish the main topic, so the embedding still points to the right content.

**Preprocessing:** HTML tags, navigation elements, scripts, and footers stripped from web sources via BeautifulSoup. PDF text cleaned of excess whitespace and form-feed characters. A garbage chunk filter skips chunks where more than 60% of tokens are single characters — this removes table cells extracted as letter sequences (e.g. "N N N T T X X") by pdfplumber.

**Final chunk count:** 6,481 chunks (after garbage filtering) across 10 sources.

---

## Sample Chunks

**Chunk 1** — Source: `cra_taulbee_survey_2023.pdf`
```
2023 Taulbee Survey. All Degree Levels Exhibit Record Number of Graduates and Strong Enrollment.
This article presents results from the 53rd annual CRA Taulbee Survey. The survey, conducted
annually by the Computing Research Association, documents trends in student enrollment, degree
production, employment of graduates, and faculty salaries in academic units in the United States
and Canada that grant the Ph.D. in computer science (CS), computer engineering (CE), or
information (I).
```

**Chunk 2** — Source: `Goldwater Scholarship`
```
From an estimated pool of over 5,000 college sophomores and juniors, 1,485 students majoring in
science, engineering, and mathematics were nominated by 482 academic institutions to compete for
the 2026 Goldwater Scholarships. Among the students who reported, 226 are men, 217 are women,
and nearly all intend to pursue a PhD as their highest degree. Of the awardees, 54 Scholars plan
to pursue research careers in mathematics and computer science, 237 in the sciences, 98 in
medicine, and 65 in engineering and materials research.
```

**Chunk 3** — Source: `Goldwater Scholarship`
```
The Goldwater Foundation is a federally endowed, independent agency established by Public Law
99-661 on November 14, 1986. The scholarship program honoring Senator Barry Goldwater was
designed to identify, encourage, and financially support outstanding undergraduates interested
in pursuing research careers in the sciences, engineering, and mathematics. The Goldwater
Scholarship is the preeminent undergraduate award of its type in these fields.
```

**Chunk 4** — Source: `salliemae_how_america_pays_2025.pdf`
```
How America Pays for College 2025. Sallie Mae's national study of college students and parents.
Conducted by Ipsos. Our mission to power confidence as students begin their unique journeys is
our north star and a reminder to be champions for students and families. We create products and
experiences that support students when they need it most.
```

**Chunk 5** — Source: `ncses_stem_workforce_survey_2023.pdf`
```
The published tables provide information on doctoral scientists and engineers by field of
doctorate and occupation; by demographic characteristics, such as sex, race, ethnicity,
citizenship, and age; by employment-related characteristics, such as sector of employment,
median annual salary, and labor-force rates; and by residency within or outside of the
United States.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers. Runs locally with no API key or rate limits. It maps text into a 384-dimensional vector space — semantically similar text ends up close together, so a query like "who qualifies for the Goldwater Scholarship" can retrieve a chunk that says "nominees must be U.S. citizens enrolled full-time in a STEM degree" even though none of those exact words appeared in the query.

**Production tradeoff reflection:** `all-MiniLM-L6-v2` has a 256-token input ceiling, meaning chunks longer than that get silently truncated before embedding — a real risk for dense policy documents. For a production system, I would consider `text-embedding-3-large` (OpenAI) for higher accuracy and longer context support. Since this tool targets students worldwide, a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2` would better serve non-English speakers. The tradeoff is cost and latency — API-based models charge per token and add network overhead, while local models like `all-MiniLM-L6-v2` are free and fast but less accurate on domain-specific text.

---

## Retrieval Test Results

**Query 1:** "What is the Goldwater Scholarship award amount?"

Top returned chunks:
- [Source: Goldwater Scholarship | Distance: 0.5651] — "the Goldwater Board will award 454 scholarships for the 2026-2027 academic year..."
- [Source: Goldwater Scholarship | Distance: 0.5735] — "one of the oldest and most prestigious national scholarships available for students in the natural sciences, mathematics, and engineering..."
- [Source: Goldwater Scholarship | Distance: 0.6356] — "...up to $7,500 in financial support. Goldwater Scholars are selected for their demonstrated research potential..."

**Why relevant:** All 3 chunks come from the Goldwater Scholarship source, directly describing the program. The $7,500 figure appears in chunk 3, confirming the answer is present. Distances are moderate (0.56–0.64), acceptable for this domain.

---

**Query 2:** "What percentage of engineering degrees are awarded to women?"

Top returned chunks:
- [Source: ncses_stem_talent_indicators.pdf | Distance: 0.4908] — "Slightly more women with a bachelor's or an advanced degree (51%) earned their highest degree in a STEM field than men..."
- [Source: ncses_stem_talent_indicators.pdf | Distance: 0.5593] — "Men earned the highest shares of degrees in engineering, accounting for at least 72% of the degrees at any level..."

**Why relevant:** Both chunks come from the NCSES STEM Talent report, directly addressing degree attainment by gender. The second chunk contains the answer (men = 72% → women ≈ 28%). Distance of 0.49 on the top result is the strongest retrieval in the evaluation set.

---

**Query 3:** "How much federal funding goes to STEM research at universities?"

Top returned chunks:
- [Source: collegeboard_trends_student_aid_2025.pdf | Distance: 0.7294] — funding figures for institutional grant aid
- [Source: ncses_federal_rd_funding_2025.pdf | Distance: 0.7387] — federal funds survey reference tables

**Why partially relevant:** The NCSES document is the right source, but the retrieved chunk is a table-of-contents reference rather than the actual funding figures. High distances (0.73+) indicate weak semantic match — this is a retrieval failure caused by the question using "STEM research" while the document uses "federal obligations for R&D."

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a STEM scholarship assistant. Answer the user's question using ONLY the
information in the provided context below. Follow these rules:

1. Base your answer only on facts that appear in the context. Do not use outside knowledge.
2. You MAY draw reasonable conclusions from the facts present — for example, if the context
   says men earned 72% of engineering degrees, you may state that women earned the remaining
   28%. Simple arithmetic and direct logical inference from the context is allowed.
3. If the context genuinely does not contain the information needed, respond exactly:
   "I don't have enough information on that in my sources."
4. For subjective questions, summarize the relevant options the context actually describes.
5. Be concise and factual.
```

A second prompt (`PARTIAL_PROMPT`) is used when the best retrieved chunk has a distance score above 0.65 — it instructs the model to share what the context does contain and suggest 2–3 related follow-up questions. If all chunks have distance above 0.85, the system returns a clean refusal without calling the LLM at all.

**How source attribution is surfaced in the response:** Source names are extracted programmatically from chunk metadata after retrieval and appended to every response. The LLM is never asked to generate or invent citations — they come directly from ChromaDB's stored metadata.

---

## Example Responses

**Example 1** — In-scope, direct answer:

> **Q:** What is the Goldwater Scholarship award amount?
>
> **A:** The Goldwater Scholarship award amount is up to $7,500 in financial support.
>
> **Retrieved from:** • Goldwater Scholarship

---

**Example 2** — In-scope, requires inference:

> **Q:** What percentage of engineering degrees are awarded to women?
>
> **A:** According to the NCSES STEM Talent report, men earned at least 72% of engineering degrees at any level. This means women earned approximately 28% or less of engineering degrees.
>
> **Retrieved from:** • ncses_stem_talent_indicators.pdf

---

**Example 3** — Out-of-scope refusal:

> **Q:** What is the capital of France?
>
> **A:** I don't have enough information on that in my sources. Try asking about STEM scholarship eligibility, award amounts, application requirements, or funding statistics.
>
> **Retrieved from:** (none)

---

## Query Interface

**Input fields:** A single text box labeled "Your question" with placeholder text suggesting example queries.

**Output fields:**
- "Answer" — the LLM-generated response grounded in retrieved context
- "Retrieved from" — a bulleted list of source document names, appended programmatically from chunk metadata

**How to run:**
```bash
python app.py
# Opens at http://localhost:7860
```

**Sample interaction transcript:**

```
User: What share of computing PhD degrees were awarded to women in 2022-23?

Answer: In the CS field, 22.7 percent of PhD degrees were awarded to women in the
2022-23 academic year. However, across CS, CE, and I fields combined, 24.1 percent
of PhD degrees were awarded to women.

Retrieved from:
• cra_taulbee_survey_2023.pdf
• ncses_stem_workforce_survey_2023.pdf
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the annual award amount for the Barry Goldwater Scholarship and how many scholarships are awarded each year? | $7,500/year; up to 410 scholarships annually | Mentioned $2.5M total + 454 scholarships for 2026-27; did not state the $7,500 per-scholar figure | Partially relevant | Partially accurate |
| 2 | What percentage of U.S. undergraduates received grant aid in the most recent reporting year, and what was the average grant amount? | 57% of undergraduate families used grant aid (AY 2024–25); ~$12,080 in grant aid per FTE undergraduate, of $16,810 total aid (College Board 2025) | "I don't have enough information on that in my sources." | Partially relevant | Inaccurate |
| 3 | What share of computing PhD degrees were awarded to women in the 2022–2023 academic year according to the CRA Taulbee Survey? | A specific percentage from the CRA Taulbee Survey | 22.7% in CS; 24.1% across CS, CE, and I combined | Relevant | Accurate |
| 4 | How much did the federal government obligate for research and development in FY 2024? | ~$202 billion in total federal R&D obligations FY 2024 (NSF NCSES Federal Funds for R&D survey summary table) | "I don't have enough information on that in my sources." | Partially relevant | Inaccurate |
| 5 | What is the eligibility GPA requirement for the Goldwater Scholarship and what fields of study qualify? | No formal GPA cutoff; fields: natural sciences, mathematics, engineering | "I don't have enough information on that in my sources." | Partially relevant | Inaccurate |

---

## Failure Case Analysis

**Question that failed:** What is the eligibility GPA requirement for the Goldwater Scholarship and what fields of study qualify?

**What the system returned:** "I don't have enough information on that in my sources." — despite `goldwaterscholarship.gov` being scraped directly as a source and producing 559 chunks.

**Root cause (tied to a specific pipeline stage):** This is a retrieval failure at the embedding stage. The query contains two sub-questions: "GPA requirement" and "fields of study." The embedding model produces a single vector that averages both concepts. The Goldwater website's eligibility text uses language like "natural sciences, mathematics, and engineering" and "sophomores and juniors" — vocabulary that doesn't semantically overlap well with "GPA requirement" or "fields of study" as phrased in the query. The most relevant chunks were ranked too low to be in the top 5. A secondary cause is that the Goldwater website produced 559 chunks — a large volume of general promotional text that dilutes the specific eligibility chunks in the ranking.

**What you would change to fix it:** Two options. First, reduce chunk size for the Goldwater website specifically — smaller chunks (150–200 characters) would isolate eligibility sentences rather than blending them with surrounding promotional content. Second, use a hybrid search approach combining semantic similarity with keyword matching (BM25) so that queries containing exact terms like "eligibility" or "fields of study" can still surface exact-match chunks even when semantic distance is high.

---

## Spec Reflection

**One way the spec helped you during implementation:**

Writing the five evaluation questions in `planning.md` *before* touching any pipeline code turned out to be the most useful thing I did. Once Milestone 4 was wired up, I had a concrete target to run retrieval against instead of poking at the system with whatever question popped into my head. The very first time I ran all five questions through `retrieve.py`, questions 2 and 4 came back with high distance scores and table-of-contents chunks instead of real figures — and that told me my table extraction was broken *before* I had built the generation layer or the UI on top of it. If I'd waited until the end to write test questions, I would have found the same failure much later, tangled up with prompt and interface bugs, and had a much harder time isolating the cause. The spec basically forced me to define "working" up front, and that definition caught a real problem early.

**One way your implementation diverged from the spec, and why:**

Two divergences, both forced by reality rather than preference. First, my plan (Milestone 3 in the AI Tool Plan) committed to **docling** for PDF parsing because it converts tables into structured markdown, which my numeric-heavy domain really needs. When I actually tried it, docling wanted a 1–2 GB model download and the first-run processing was painfully slow on my hardware, so I fell back to **pdfplumber**. That fallback is the direct cause of my biggest failure case: pdfplumber reads tables left-to-right with no sense of structure, so the Federal R&D document came through as raw number rows with the column headers stripped off (you can see this in the chunks — years like `2024` followed by bare figures in thousands, no labels). The honest version of events is that the spec was right about *what* I needed, I couldn't afford it, so I shipped a worse parser and documented the consequence rather than hiding it.

Second, my chunking spec said **500 tokens / 50 token overlap**, but the implementation in `ingest.py` actually splits on **500 characters / 50 characters**. That's because I used LangChain's `RecursiveCharacterTextSplitter` with its default `length_function=len`, which counts characters, not tokens — I never plugged in a tokenizer. I noticed the mismatch only after the fact. In practice 500 characters (~80–100 words) is smaller than the 500 tokens I'd planned, and that accident actually works *with* the embedding model instead of against it: `all-MiniLM-L6-v2` truncates at 256 tokens anyway, so a 500-character chunk almost never overflows the model's input ceiling, whereas a true 500-token chunk would have lost its back half on every single embedding. A mistake that happened to dodge the exact truncation risk I'd flagged in planning.

---

## AI Usage

**Instance 1 — Ingestion and the garbage-chunk filter**

- *What I gave the AI:* I pasted the Documents and Chunking Strategy sections from `planning.md` and asked Claude to write `ingest.py` — load every PDF, strip web HTML with BeautifulSoup, split with `RecursiveCharacterTextSplitter` at my chunk size and overlap, and attach `source` + `chunk_index` metadata to each chunk so attribution would work downstream.
- *What it produced:* A clean first draft of the loader and splitter. But when I ran it and dumped the output to `chunks_preview.txt`, a big share of the PDF chunks were nonsense — strings like `N N N T T X X` where pdfplumber had read table cells letter-by-letter, plus rows of bare numbers from statistical tables. Claude's initial version happily embedded all of it.
- *What I changed or overrode:* This is where I had to direct rather than accept. I showed Claude examples of the bad chunks and asked it for a way to detect them. We landed on `is_garbage()` — skip any chunk where more than 60% of the whitespace-separated tokens are single characters. I picked the 0.6 threshold myself by eyeballing the preview file: lower values were throwing away legitimate prose that happened to contain initials and single-letter variables, higher values let the `N N N T T` rows back in. I also overrode my own original plan here — the spec said docling, but after the hardware issues I told Claude to keep pdfplumber and treat the garbage filter as the mitigation instead. It's a patch over a parser problem, not a real fix, and I noted that limitation honestly in the README.

**Instance 2 — The three-tier grounding / refusal logic**

- *What I gave the AI:* I gave Claude the full `planning.md`, my `retrieve()` function, and the Gradio skeleton, and asked it to wire `generate.py` to Groq's `llama-3.3-70b-versatile` with a system prompt that answers only from retrieved context and refuses when the answer isn't there.
- *What it produced:* A working single-prompt version: retrieve top-k, stuff the chunks into one grounding prompt, and either answer or return the fixed "I don't have enough information" line. Functionally correct, but in testing it behaved like a light switch — for partial-match questions where the context *almost* covered the answer, it would flatly refuse and give the user nothing, even though there was relevant material sitting right there in the retrieved chunks.
- *What I changed or overrode:* I redesigned the control flow into three tiers gated on the retrieval distance score, which I added on top of Claude's draft: below 0.65 the normal `SYSTEM_PROMPT` runs; between 0.65 and 0.85 a second `PARTIAL_PROMPT` kicks in that shares what context *does* exist and suggests 2–3 follow-up questions the sources can actually answer; above 0.85 the system returns a hard refusal *without even calling the LLM*, which saves a wasted API round-trip on clearly out-of-scope queries. I chose both thresholds by reading the actual distance scores off my `retrieve.py` test runs and finding where on-topic and off-topic results separated. I also overrode one thing on principle: I would not let the model generate its own source citations. The "Retrieved from" list is built programmatically from ChromaDB metadata (`dict.fromkeys` to dedupe while keeping order) so the model literally cannot hallucinate a source — it only ever sees the question and the context, never the citation logic.
