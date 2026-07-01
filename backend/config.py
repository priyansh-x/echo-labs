import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
TICK_DELAY = 1.0
MAX_TICKS = 200
MAP_WIDTH = 5
MAP_HEIGHT = 5
