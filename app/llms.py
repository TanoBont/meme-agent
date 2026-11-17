
from langchain_openai import ChatOpenAI

from app.config import OPENAI_MODEL


def get_openai_model(temperature=0.7):
    """
    Crea e restituisce un modello linguistico OpenAI.
    """
    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=temperature
    )
