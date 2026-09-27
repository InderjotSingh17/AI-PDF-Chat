import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )
client = genai.Client(
    api_key=GEMINI_API_KEY
)
def generate_answer(
    question: str,
    context: str,
    history: str = ""
):
    """
    Generate an answer using the retrieved PDF context
    and previous conversation history.
    """
    prompt = f"""
You are an AI assistant that answers questions about uploaded PDF documents.
Rules:
1. Answer using the provided PDF context.
2. Do not invent information.
3. If the answer is not present in the context, say:
   "I could not find this information in the uploaded document."
4. Keep the answer clear and useful.
5. Use previous conversation only when it helps understand the current question.
Previous conversation:
{history}
PDF context:
{context}
User question:
{question}
Answer:
"""
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    return response.text