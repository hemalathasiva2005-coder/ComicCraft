from pathlib import Path
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.schemas import PromptRequest
from app.gemini_flash import generate_outline, generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf
router=APIRouter(); BASE_DIR=Path(__file__).resolve().parent.parent; templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))
def create_comic(payload):
    outline=generate_outline(payload.story_prompt,payload.character_name,payload.setting,payload.tone,payload.art_style)
    story=generate_story(outline,payload.character_name,payload.tone)
    images=[generate_image(p["image_prompt"],p["panel_number"],payload.art_style) for p in outline]
    layout=build_comic_layout(outline,story,images); return layout,save_pdf(layout)
@router.get("/",response_class=HTMLResponse)
async def home(request:Request): return templates.TemplateResponse(request=request,name="index.html",context={"request":request})
@router.post("/generate",response_class=HTMLResponse)
async def generate(request:Request,story_prompt:str=Form(...),character_name:str=Form(...),setting:str=Form(...),tone:str=Form(...),art_style:str=Form(...)):
    try:
        payload=PromptRequest(story_prompt=story_prompt,character_name=character_name,setting=setting,tone=tone,art_style=art_style)
        layout,pdf_path=create_comic(payload)
        return templates.TemplateResponse(request=request,name="comic_preview.html",context={"request":request,"layout":layout,"pdf_path":pdf_path})
    except Exception as exc:
        return templates.TemplateResponse(request=request,name="index.html",context={"request":request,"error":f"Generation failed: {exc}"},status_code=500)
@router.post("/generate-comic/json")
async def generate_json(payload:PromptRequest):
    layout,pdf_path=create_comic(payload); return {"success":True,"panels":layout,"pdf_path":pdf_path}
@router.get("/export-success",response_class=HTMLResponse)
async def export_success(request:Request,pdf:str=""): return templates.TemplateResponse(request=request,name="export_success.html",context={"request":request,"pdf_path":pdf})
@router.get("/test-image")
async def test_image(prompt:str="A brave fox exploring an enchanted forest, comic art"):
    try: return {"success":True,"image_path":generate_image(prompt,0,"comic book")}
    except Exception as exc: raise HTTPException(status_code=500,detail=str(exc))
@router.get("/download/{filename}")
async def download_pdf(filename:str):
    base=(BASE_DIR/"static"/"exports").resolve(); target=(base/filename).resolve()
    if target.parent!=base or target.suffix.lower()!=".pdf" or not target.exists(): raise HTTPException(status_code=404,detail="PDF not found.")
    return FileResponse(target,media_type="application/pdf",filename=target.name)
