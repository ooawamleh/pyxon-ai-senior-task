import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import backend.config as config

# Initialize the search wrapper to pull 40 results deep, ensuring our Post-Filter finds trusted domains
serp = SerpAPIWrapper(params={"engine": "google", "num": 40})

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def url_api_fetcher(url: str) -> str:
    """Fetches and cleans content from URLs or APIs."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Check if JSON API
        if 'application/json' in response.headers.get('Content-Type', ''):
            return f"[API DATA from {url}]:\n{response.json()}"
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        return f"[WEBPAGE DATA from {url}]:\n{text[:6000]}" # Limit context
    except Exception as e:
        return f"[FETCH ERROR for {url}]: {str(e)}"

def multi_query_ephemeral_rag(queries: list) -> str:
    """Agent 3: Executes multi-query search and builds Ephemeral RAG (Post-Search Filtering)."""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    all_organic_results = []
    
    # 1. Search broadly to catch breaking news without overloading Google's boolean logic
    for q in queries:
        full_query = q
        try:
            results = serp.results(full_query).get("organic_results", [])
            all_organic_results.extend(results)
        except:
            continue
            
    if not all_organic_results:
        return "No high-confidence intelligence found."

    # 2. Deduplicate all results
    df = pd.DataFrame(all_organic_results).drop_duplicates(subset=['link'])
    
    # 3. SENIOR TRICK: Post-Search Domain Filtering
    # Only keep results that belong to our trusted domains list
    trusted_domains_pattern = '|'.join([domain.replace('.', r'\.') for domain in config.TRUSTED_DOMAINS])
    df = df[df['link'].str.contains(trusted_domains_pattern, case=False, na=False)]
    
    if df.empty or 'snippet' not in df.columns:
        return "Intelligence was found, but none matched our Verified Trusted Domains network."
        
    df = df[['title', 'link', 'snippet']].dropna()
    
    documents = [
        Document(page_content=row['snippet'], metadata={"source": row['link'], "title": row['title']})
        for _, row in df.iterrows()
    ]
    
    # 4. Ephemeral Vector DB
    vector_db = FAISS.from_documents(documents, embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 10}) # Get top 10 relevant contexts
    
    # Retrieve best context based on the user's primary intent (first query)
    relevant_docs = retriever.invoke(queries[0])
    
    context = f"Verified Intel (Date: {current_date}):\n\n"
    for i, doc in enumerate(relevant_docs):
        context += f"Doc {i+1}: {doc.metadata['title']}\nSnippet: {doc.page_content}\nSource: {doc.metadata['source']}\n---\n"
    return context