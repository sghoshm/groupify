# backend/app/main.py
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
import os
# Import the API router
from .api.v1.api import api_router
# Import the function to get the Supabase client using absolute path
from backend.app.utils.supabase_client import get_supabase_client
# Import CORS middleware if you need to handle cross-origin requests
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from the .env file in the project root
# This needs to be called before accessing os.getenv()
load_dotenv()

# Initialize the FastAPI application
app = FastAPI()

# Configure CORS middleware
# This allows your frontend running on a different origin (e.g., localhost:3000 for Flutter web)
# to make requests to your backend API.
# Adjust the allow_origins list to restrict access in production.
origins = [
    "http://localhost", # Allow requests from localhost
    "http://localhost:8000", # Allow requests from localhost on port 8000
    "http://localhost:3000", # Allow requests from a common frontend development port
    # Add the URL of your deployed frontend here in production
    # "https://your-frontend-url.cloudflarepages.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # List of allowed origins
    allow_credentials=True, # Allow cookies/authorization headers
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)


# Include the API router with a prefix for versioning
# This line is correct as it is importing from the .api package
app.include_router(api_router, prefix="/api/v1")

# Define a basic health check endpoint
@app.get("/health")
def health_check():
    """
    Basic health check endpoint.
    Returns a simple status message to indicate the service is running.
    """
    return {"status": "ok"}

# Define the root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint for the backend API.
    Returns a welcome message.
    """
    return {"message": "Welcome to Groupify Backend"}

# Application startup event
# This function runs when the FastAPI application starts up
@app.on_event("startup")
async def startup_event():
    """
    Startup event to perform initialization tasks.
    Currently includes a check to verify the Supabase connection.
    """
    print("Backend starting up...")
    try:
        # Attempt to get a Supabase client instance using the configured settings.
        # This implicitly tests if the SUPABASE_URL and SUPABASE_KEY are valid
        # and if the application can reach the Supabase API.
        supabase = get_supabase_client()

        # A more robust check might involve a trivial query on a table
        # that is publicly readable (if you have one) or a table where
        # the service role key (if you were using it here) has read access.
        # For now, successful client creation is a good initial sign.

        print("Successfully initialized Supabase client using provided credentials.")

        # Optional: You could add a check for the Ollama endpoint here as well
        # from backend.app.utils.ollama_client import generate_text_with_ollama # Use absolute path
        # try:
        #     test_ollama = generate_text_with_ollama("hello", model="llama2") # Use a small model if possible
        #     if test_ollama:
        #         print("Successfully connected to Ollama endpoint.")
        #     else:
        #         print("Warning: Could not get a response from Ollama endpoint.")
        # except Exception as ollama_e:
        #      print(f"Error connecting to Ollama endpoint: {ollama_e}")


    except Exception as e:
        # If there's any exception during Supabase client initialization,
        # print an error message. This indicates a problem with the URL, Key,
        # network connectivity, or Supabase service availability.
        print(f"Error connecting to Supabase: {e}")
        # Depending on how critical the DB connection is at startup,
        # you might want to raise the exception to prevent the app from starting.
        # raise e


# Application shutdown event
# This function runs when the FastAPI application is shutting down
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event to perform cleanup tasks.
    (Currently no specific cleanup needed for Supabase client).
    """
    print("Backend shutting down...")
    # Add any necessary cleanup code here, e.g., closing custom connections
