# backend/app/core/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file (important for local development)
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://kuskatygbvqcekuhtirp.supabase.co")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1c2thdHlnYnZxY2VrdWh0aXJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5MzQxMjgsImV4cCI6MjA1OTUxMDEyOH0.paoBmQHSEerJI5WYA6Zp18fBTNM7mrKeqiKKc8ikYlg") # Use anon key here
    OLLAMA_ENDPOINT: str = os.getenv("OLLAMA_ENDPOINT", "http://ollama:11434")

    # Add other settings as needed (e.g., database connection details if not Supabase)
    # SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey") # Example for JWT signing

settings = Settings()

# Basic check to warn if default placeholders are used
if settings.SUPABASE_URL == "YOUR_SUPABASE_URL" or settings.SUPABASE_KEY == "YOUR_SUPABASE_KEY":
    print("WARNING: Using default Supabase URL or Key. Please configure your .env file.")
if settings.OLLAMA_ENDPOINT == "http://ollama:11434":
     print("INFO: Using default Ollama endpoint. Ensure it's accessible.")
