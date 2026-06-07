import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "stem_scholarships"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

model = SentenceTransformer(EMBED_MODEL)
client = chromadb.PersistentClient(path="chroma_store")
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query: str) -> list[dict]:
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "distance": round(dist, 4),
        })
    return chunks


if __name__ == "__main__":
    test_queries = [
        "What is the Goldwater Scholarship award amount?",
        "What percentage of engineering degrees are awarded to women?",
        "How much federal funding goes to STEM research at universities?",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        for i, chunk in enumerate(retrieve(query)):
            print(f"[{i+1}] Source: {chunk['source']} | Distance: {chunk['distance']}")
            print(chunk["text"][:300])
            print()
