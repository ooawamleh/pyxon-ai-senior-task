import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import backend.config as config

CACHE_PATH = "semantic_cache_index"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_or_create_cache():
    if os.path.exists(CACHE_PATH):
        return FAISS.load_local(CACHE_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        # Create an empty vector store initialized with a dummy doc
        dummy_doc = Document(page_content="dummy_init", metadata={"answer": "dummy"})
        db = FAISS.from_documents([dummy_doc], embeddings)
        return db

cache_db = load_or_create_cache()

def check_cache(query: str, threshold: float = 0.6):
    """Agent 6: Fetch potential cache matches for the LLM to evaluate."""
    results = cache_db.similarity_search_with_score(query, k=1)
    if results:
        doc, score = results[0]
        if score < threshold and doc.page_content != "dummy_init":
            # Return BOTH the cached query and the answer
            return {"cached_query": doc.page_content, "cached_answer": doc.metadata["answer"]}
    return None

def save_to_cache(query: str, answer: str):
    """Agent 6: Save successful query-answer pairs."""
    new_doc = Document(page_content=query, metadata={"answer": answer})
    cache_db.add_documents([new_doc])
    cache_db.save_local(CACHE_PATH)