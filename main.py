from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
app=FastAPI(title="ComicCraft - AI Comic Story Creator")
BASE_DIR=Path(__file__).resolve().parent.parent
app.mount("/static",StaticFiles(directory=str(BASE_DIR/"static")),name="static")
app.include_router(router)
