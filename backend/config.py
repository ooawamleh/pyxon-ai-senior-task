# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===========================
# CONFIGURATION
# ===========================
# Now we fetch the keys safely from the environment
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

# Global Constants - Expanded Trusted Domains (Global & Arab News + Defense)
TRUSTED_DOMAINS = [
    # Global Defense & Think Tanks
    "understandingwar.org", "rusi.org", "chathamhouse.org", "iiss.org", 
    "eurasiagroup.net", "janes.com", "breakingdefense.com", "navalnews.com", "defensenews.com",
    
    # Global News
    "reuters.com", "apnews.com", "bloomberg.com", "bbc.com", "bbc.co.uk", 
    "cnn.com", "nytimes.com", "washingtonpost.com", "theguardian.com", 
    "wsj.com", "ft.com", "afp.com",
    
    # Middle East / Arab News
    "aljazeera.net", "aljazeera.com", "alarabiya.net", "skynewsarabia.com", 
    "asharq.com", "independentarabia.com", "rtarabic.com", "france24.com",
    
    # Specific Regional
    "kyivindependent.com", "scmp.com"
]

# Silence Transformers and HuggingFace warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import warnings
warnings.filterwarnings("ignore", category=UserWarning)