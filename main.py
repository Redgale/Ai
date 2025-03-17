from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import logging
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Enable CORS for your Neocities frontend
origins = [
    "https://ai-fronthead.neocities.org",  # Your Neocities site URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],             # Allows all HTTP methods
    allow_headers=["*"],             # Allows all headers
)

# Load API key from environment variables (set in Koyeb dashboard)
API_KEY = os.getenv("AI_API_KEY")
API_URL = "https://api.openai.com/v1/completions"  # Change this if using another AI API

# Define a Pydantic model for the JSON body
class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    logging.debug("Home route accessed")
    return {"message": "AI API is running!"}

@app.post("/generate")
def generate(req: PromptRequest):
    prompt = req.prompt
    logging.debug(f"Generate route accessed with prompt: {prompt}")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-davinci-003",  # Change model if needed
        "prompt": prompt,
        "max_tokens": 100
    }
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error response: {response.text}")
        return {"error": response.text}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
