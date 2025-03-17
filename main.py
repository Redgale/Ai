from fastapi import FastAPI
import requests
import os

app = FastAPI()

# Load API key from environment variables (set in Koyeb dashboard)
API_KEY = os.getenv("AI_API_KEY")
API_URL = "https://api.openai.com/v1/completions"  # Change this if using another AI API

@app.get("/")
def home():
    return {"message": "AI API is running!"}

@app.post("/generate")
def generate(prompt: str):
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
        return {"error": response.text}
