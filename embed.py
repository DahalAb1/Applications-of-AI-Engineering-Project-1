import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_pdfs, load_websites

COLLECTION_NAME = "stem_scholarships"
EMBED_MODEL = "all-MiniLM-L6-v2"


def build_vector_store():
    print("Loading chunks...")
    chunks = load_pdfs() + load_websites()
    print(f"Total chunks to embed: {len(chunks)}")

    print(f"Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path="chroma_store")

    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
        print("Existing collection deleted.")

    collection = client.create_collection(COLLECTION_NAME)

    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    ids = [f"{c['source']}_{c['chunk_index']}" for c in chunks]

    print("Embedding chunks (this may take a minute)...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    batch_size = 5000
    for i in range(0, len(chunks), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=texts[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            metadatas=[{"source": s} for s in sources[i:i+batch_size]],
        )
        print(f"  Stored batch {i // batch_size + 1}")

    print(f"\nDone. {len(chunks)} chunks stored in ChromaDB collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    build_vector_store()
