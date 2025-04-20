from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow all origins for Copilot Studio to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ComplaintsInput(BaseModel):
    complaints: str

@app.post("/summarize")
async def summarize_complaints(data: ComplaintsInput):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You summarize user complaints into bullet points."},
                {"role": "user", "content": data.complaints}
            ],
            temperature=0.3
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}