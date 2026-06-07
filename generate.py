import os
from dotenv import load_dotenv
from groq import Groq
from retrieve import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

OUT_OF_SCOPE_THRESHOLD = 0.85  # all chunks beyond this = truly out of scope
PARTIAL_THRESHOLD = 0.65       # best chunk beyond this = partial match, suggest follow-ups

SYSTEM_PROMPT = """You are a STEM scholarship assistant. Answer the user's question \
using ONLY the information in the provided context below. Follow these rules:

1. Base your answer only on facts that appear in the context. Do not use outside knowledge.
2. You MAY draw reasonable conclusions from the facts present — for example, if the \
context says men earned 72% of engineering degrees, you may state that women earned \
the remaining 28%. Simple arithmetic and direct logical inference from the context is allowed.
3. If the context genuinely does not contain the information needed, respond exactly: \
"I don't have enough information on that in my sources."
4. For subjective questions (e.g. "what is the best scholarship?"), do not invent an \
opinion. Instead, summarize the relevant options the context actually describes.
5. Be concise and factual.

Context:
{context}"""

PARTIAL_PROMPT = """You are a STEM scholarship assistant. The user asked a question \
that your sources only partially address. Follow these rules:

1. Share what the context DOES contain that is relevant — even if it doesn't directly \
answer the question. Use only facts from the context, no outside knowledge.
2. After your answer, add a short section: "You might also want to ask:" and suggest \
2–3 specific follow-up questions that your sources CAN answer based on the context provided.
3. Be honest that the match is partial.

Context:
{context}"""


def ask(question: str) -> dict:
    chunks = retrieve(question)
    best_distance = chunks[0]["distance"] if chunks else 1.0

    # Truly out of scope — all retrieved chunks are too distant
    if best_distance > OUT_OF_SCOPE_THRESHOLD:
        return {
            "answer": "I don't have enough information on that in my sources. Try asking about STEM scholarship eligibility, award amounts, application requirements, or funding statistics.",
            "sources": [],
            "chunks": chunks,
        }

    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )

    # Partial match — use the suggestion-aware prompt
    prompt = PARTIAL_PROMPT if best_distance > PARTIAL_THRESHOLD else SYSTEM_PROMPT

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt.format(context=context)},
            {"role": "user", "content": question},
        ],
        temperature=0.1,
    )

    answer = response.choices[0].message.content
    unique_sources = list(dict.fromkeys(c["source"] for c in chunks))

    return {
        "answer": answer,
        "sources": unique_sources,
        "chunks": chunks,
    }


if __name__ == "__main__":
    test_questions = [
        "What is the Goldwater Scholarship award amount?",
        "What percentage of engineering degrees are awarded to women?",
        "What is the capital of France?",  # out-of-scope — should refuse
    ]

    for q in test_questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        print("-" * 60)
        result = ask(q)
        print(f"A: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
