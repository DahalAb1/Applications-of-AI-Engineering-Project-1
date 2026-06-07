import os
import re
import pdfplumber
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter



"""
Problems found in chunking : 

1. Chunking did not extract monetary value, $ signs
2. Percentages, and numeric symbols were ignored, therefore, some numbers lost their significance 
3. My RAG is heavily dependent on numeric data so this should be handled more carefully
4. Chunking data from table and chart lost meaning when they were transcribed as text by pdfplumber  
"""

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

WEBSITES = [
    {"url": "https://goldwaterscholarship.gov", "source": "Goldwater Scholarship"},
    {"url": "https://opportunitydesk.org", "source": "Opportunity Desk"},
]


def clean_text(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\x0c', '', text)  # remove form feed characters from PDFs
    return text.strip()


def load_pdfs() -> list[dict]:
    chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    for filename in os.listdir(DOCUMENTS_DIR):
        if not filename.endswith(".pdf"):
            continue

        filepath = os.path.join(DOCUMENTS_DIR, filename)
        print(f"Loading {filename}...")

        with pdfplumber.open(filepath) as pdf:
            pages = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)

        if not pages:
            print(f"  WARNING: no text extracted from {filename} (may be scanned)")
            continue

        full_text = clean_text("\n\n".join(pages))
        splits = splitter.split_text(full_text)

        for i, chunk in enumerate(splits):
            if len(chunk.strip()) > 0:
                chunks.append({
                    "text": chunk,
                    "source": filename,
                    "chunk_index": i,
                })

        print(f"  → {len(splits)} chunks")

    return chunks


def load_websites() -> list[dict]:
    chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    for site in WEBSITES:
        print(f"Fetching {site['source']}...")
        try:
            response = requests.get(site["url"], timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = clean_text(soup.get_text(separator="\n"))
            splits = splitter.split_text(text)

            for i, chunk in enumerate(splits):
                if len(chunk.strip()) > 0:
                    chunks.append({
                        "text": chunk,
                        "source": site["source"],
                        "chunk_index": i,
                    })

            print(f"  → {len(splits)} chunks")
        except Exception as e:
            print(f"  ERROR fetching {site['source']}: {e}")

    return chunks


if __name__ == "__main__":
    pdf_chunks = load_pdfs()
    web_chunks = load_websites()
    all_chunks = pdf_chunks + web_chunks

    print(f"\nTotal chunks: {len(all_chunks)}")

    with open("chunks_preview.txt", "w", encoding="utf-8") as f:
        f.write(f"Total chunks: {len(all_chunks)}\n")
        f.write("=" * 60 + "\n\n")
        for chunk in all_chunks:
            f.write(f"[Source: {chunk['source']} | Chunk #{chunk['chunk_index']}]\n")
            f.write(chunk["text"])
            f.write("\n\n" + "-" * 60 + "\n\n")

    print("Chunks saved to chunks_preview.txt")
