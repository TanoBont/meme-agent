import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Configurazione workflow
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "2"))
MAX_TRENDS = int(os.getenv("MAX_TRENDS", "5"))
