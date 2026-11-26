
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from google import genai

app = FastAPI(title="CareerAI Navigator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kameshwar333354.github.io"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


class CareerQuestion(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "CareerAI Navigator backend is running!"
    }


@app.post("/ask")
def ask_career_ai(question: CareerQuestion):

    if not client:
        return {
            "error": "AI API key is not configured yet."
        }

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                "You are CareerAI Navigator, a helpful career guidance "
                "assistant. Give clear, practical and balanced guidance. "
                "Do not guarantee jobs, salaries or admission outcomes. "
                "Encourage students to verify important education and "
                "career information with official sources.\n\n"
                f"User question: {question.message}"
            )
        )

        return {
            "answer": response.text
        }

    except Exception:
        return {
            "error": "The AI service is temporarily unavailable. Please try again."
        }
