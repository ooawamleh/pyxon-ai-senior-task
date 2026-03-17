import re
import os
import datetime
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from backend.src.prompts import clarify_prompt, expand_prompt, synthesize_prompt, final_response_prompt
from backend.src.tools import multi_query_ephemeral_rag, url_api_fetcher
from backend.src.cache_manager import check_cache, save_to_cache
import backend.config as config

# Initialize Core LLM via OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openrouter/free",
    temperature=0.1
)

# Define Agent Chains (LCEL)
clarifier_chain = clarify_prompt | llm | StrOutputParser()
expander_chain = expand_prompt | llm | StrOutputParser()
synthesizer_chain = synthesize_prompt | llm | StrOutputParser()
responder_chain = final_response_prompt | llm | StrOutputParser()

# Agent 6.5: The Cache Evaluator (Intent Matcher)
# ==========================================
cache_eval_prompt = PromptTemplate.from_template(
    """You are a strict Cache Evaluator. 
    User's NEW Query: '{new_query}'
    User's OLD Cached Query: '{cached_query}'
    
    Task: Do these two queries ask for the EXACT same information or intent? 
    (e.g., "latest updates" is NOT the same as "how it started").
    
    Answer ONLY 'YES' or 'NO'. Do not explain.
    """
)
cache_eval_chain = cache_eval_prompt | llm | StrOutputParser()

def extract_urls(text: str) -> list:
    """Helper to find URLs in user query"""
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.findall(text)

def run_gil_swarm(user_query: str, history: str) -> str:
    """The Swarm Orchestrator managing Agents 1 to 6."""
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    print(f"\n🧠 [Swarm Orchestrator] Starting analysis for: '{user_query}' (Date: {current_date})")
    
# 1. Agent 6 & 6.5: Check Cache and Evaluate Intent
    cached_data = check_cache(user_query)
    if cached_data:
        cached_query = cached_data["cached_query"]
        cached_answer = cached_data["cached_answer"]
        
        print(f"🤔 [Agent 6.5] FAISS found a similar old query: '{cached_query}'. Evaluating intent...")
        
        is_match = cache_eval_chain.invoke({
            "new_query": user_query,
            "cached_query": cached_query
        }).strip().upper()
        
        if "YES" in is_match:
            # 🛡️ THE SELF-HEALING CHECK (Read Protection)
            error_indicators = [
                "GIL Protocol Error", 
                "No high-confidence intelligence", 
                "does not provide information",
                "No actionable or confirmed intelligence",
                "rather than detailing"
            ]
            is_poisoned = any(indicator.lower() in cached_answer.lower() for indicator in error_indicators)
            
            if is_poisoned:
                print("☣️ [Agent 6.5] Intent matched, but cached data is POISONED. Bypassing cache to fetch fresh data...")
            else:
                print("⚡ [Agent 6.5] LLM verified Cache HIT! Data is healthy.")
                return f"[⚡ Retrived from Verified Semantic Cache]\n\n{cached_answer}"
        else:
            print("⏳ [Agent 6.5] LLM rejected Cache match (Different intents). Proceeding to Agent 1...")
    else:
        print("⏳ [Agent 6] Cache empty for this topic. Proceeding to Agent 1.")


# 2. Agent 1: Clarify (Injecting Memory)
    print("-> Agent 1: Checking for clarification...")
    clarified_query = clarifier_chain.invoke({
        "history": history,
        "query": user_query,
        "current_date": current_date
    }).strip()
    if clarified_query == "UNCLEAR":
        return "GIL Protocol Error: Query unclear. Please provide more context or specific intelligence parameters."

    # 3. Agent 2: Expand Query
    print("📈 [Agent 2] Expanding query into search strategies...")
    expanded_str = expander_chain.invoke({
        "clear_query": clarified_query,
        "current_date": current_date
        })
    search_queries = [q.strip() for q in expanded_str.split('|') if q.strip()]
    if not search_queries:
        search_queries = [clarified_query] # Fallback
    print(f"✅ [Agent 2] Search Strategies: {search_queries}")

    # 4. Agent 3: Search & Fetch
    # A. Multi-Query Ephemeral RAG
    print(f"-> Agent 3: Fetching intel for: {search_queries}")
    rag_context = multi_query_ephemeral_rag(search_queries)
    
    # B. Fetch URLs if user provided any
    urls = extract_urls(user_query)
    url_context = ""
    if urls:
        print(f"🔗 [Agent 3] Fetching URLs: {urls}")
        for url in urls:
            url_context += url_api_fetcher(url) + "\n"

    # 5. Agent 4: Synthesize & Merge (Compare results & handle multimodal)
    print("-> Agent 4: Synthesizing and merging data...")
    raw_synthesis = synthesizer_chain.invoke({
        "original_query": user_query,
        "rag_context": rag_context,
        "url_context": url_context or "No direct URLs provided by user."
    })
    print("✅ [Agent 4] Raw Synthesis Complete.")

    # 6. Agent 5: Final Responder Formatting (Now aware of original query)
    print("✍️ [Agent 5] Formatting final SITREP/Analysis...")
    final_response = responder_chain.invoke({
        "original_query": user_query,
        "raw_synthesis": raw_synthesis
    })
    print("✅ [Agent 5] Final Response Ready.")
    return final_response

def finalize_cache(user_query, final_response):
    error_indicators = ["GIL Protocol Error", "No high-confidence intelligence", "rather than detailing", "does not provide information", "No actionable or confirmed intelligence"]
    is_poor_quality = any(indicator.lower() in final_response.lower() for indicator in error_indicators)
    
    if not is_poor_quality and "Sources:" in final_response:
        save_to_cache(user_query, final_response)
        print("💾 [Background Task] Quality Gate PASSED. Cache saved in background.")
    else:
        print("🚫 [Background Task] Quality Gate FAILED. Cache skipped.")