
from langchain_openai import ChatOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL


def get_openai_model(temperature=0.7):
    """
    Crea e restituisce un modello linguistico OpenAI.
    """

    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY non configurata. Controlla il file .env."
        )

    if OPENAI_MODEL.startswith("gpt-6"):
        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            use_responses_api=True,
            reasoning={"effort": "low"}
        )

    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=temperature,
        api_key=OPENAI_API_KEY
    )
