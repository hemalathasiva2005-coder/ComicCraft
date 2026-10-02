import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_OUTLINE_MODEL = os.getenv("GEMINI_OUTLINE_MODEL", "gemini-3.8-flash").strip()
GEMINI_STORY_MODEL = os.getenv("GEMINI_STORY_MODEL", "gemini-3.8-flash").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_IMAGE_MODEL = os.getenv("HF_IMAGE_MODEL", "stabilityai/stable-diffusion-xl-base-1.0").strip()
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "768"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "768"))
IMAGE_STEPS = int(os.getenv("IMAGE_STEPS", "20"))
def validate_required_keys(require_images=False):
    if not GEMINI_API_KEY: raise RuntimeError("GEMINI_API_KEY is missing in .env")
    if require_images and not HF_TOKEN: raise RuntimeError("HF_TOKEN is missing in .env")
