from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from utils import search_index
import openai
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Make sure your OpenAI key is set as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # OR hardcode if testing

class Query(BaseModel):
    question: str
    image: Optional[str] = None

@app.post("/api/")
def answer_question(query: Query):
    question = query.question
    relevant_docs = search_index(question)

    context = "\n\n".join(doc["content"] for doc in relevant_docs)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful TA answering based on the course and forum content."},
                {"role": "user", "content": f"Question: {question}\n\nRelevant content:\n{context}"}
            ]
        )

        answer = response.choices[0].message["content"]

        return {
            "answer": answer,
            "links": [
                {"url": doc["url"], "text": doc.get("title", "Related post")}
                for doc in relevant_docs
            ]
        }

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/")
def root():
    return {"message": "TDS Virtual TA is running!"}