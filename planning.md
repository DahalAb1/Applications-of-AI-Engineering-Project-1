# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This RAG system covers undergraduate STEM scholarships — eligibility criteria, award amounts, deadlines, and application requirements across federal, institutional, and private programs. The knowledge is hard to find in one place because opportunities are scattered across hundreds of individual program websites, government portals, and nonprofit pages, with no single authoritative source that aggregates them. Students who don't know the right organizations to search often miss scholarships they qualify for entirely.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Goldwater Scholarship | Details on the most prestigious undergrad STEM scholarship — eligibility, criteria, application process | https://goldwaterscholarship.gov |
| 2 | Opportunity Desk | Broad international STEM opportunities; useful for non-US students | https://opportunitydesk.org |
| 3 | College Board Trends in Student Aid 2025 | How much aid exists, what types, trends over time | documents/collegeboard_trends_student_aid_2025.pdf |
| 4 | Sallie Mae — How America Pays for College 2025 | How families actually fund college; financial need context | documents/salliemae_how_america_pays_2025.pdf |
| 5 | NCSES STEM Talent: Education, Training & Workforce | Who enters STEM, demographics, diversity gaps | documents/ncses_stem_talent_indicators.pdf |
| 6 | NCSES Survey of Doctorate Recipients 2023 | STEM/physics workforce outcomes, employment, salaries by field | documents/ncses_stem_workforce_survey_2023.pdf |
| 7 | Lumina Foundation — Some College, No Credential 2025 | Equity gaps, completion rates by demographic | documents/lumina_some_college_no_credential_2025.pdf |
| 8 | NCSES Federal R&D Funding FY 2024–25 | Federal STEM investment and undergraduate funding | documents/ncses_federal_rd_funding_2025.pdf |
| 9 | NCES Trends in Graduate Degrees by Field 2024 | STEM enrollment and degree attainment statistics | documents/nces_stem_enrollment_trends.pdf |
| 10 | CRA Taulbee Survey 2022–2023 | Computing-specific field data and funding pipeline | documents/cra_taulbee_survey_2023.pdf |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->
     Chunk size depends on the model's token size, and we also have to be careful to not let context change when we decide on chunks. What would a proper size be? 

Guiding questions — use these to think it through before deciding:
- Are your documents short reviews (1–3 sentences) or long guides (many paragraphs)? How does that affect the right chunk size?
- If a key fact spans two adjacent chunks, will either chunk be retrievable on its own? What does overlap help with?
- How would you know if your chunks are too small? Too large? What would bad retrieval results look like in each case?


**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
