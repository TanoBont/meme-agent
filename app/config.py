
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "2"))
MAX_TRENDS = int(os.getenv("MAX_TRENDS", "5"))
