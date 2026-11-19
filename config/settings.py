# config/settings.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Change the model in .env (GROQ_MODEL), never in code
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def get_llm(temperature: float = 0.3) -> ChatGroq:
    """Single place where the LLM is created for all agents."""
    return ChatGroq(
        model       = GROQ_MODEL,
        temperature = temperature,
        api_key     = os.environ["GROQ_API_KEY"],
    )