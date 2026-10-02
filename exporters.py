from pathlib import Path
from datetime import datetime
from fpdf import FPDF
BASE_DIR=Path(__file__).resolve().parent.parent
EXPORT_DIR=BASE_DIR/"static"/"exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
def clean_text(value): return str(value).encode("latin-1","replace").decode("latin-1")
def save_pdf(layout):
    filename="comic_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".pdf"; path=EXPORT_DIR/filename; pdf=FPDF()
    for panel in layout:
        pdf.add_page(); pdf.set_font("Arial","B",18); pdf.cell(0,12,clean_text(f"Panel {panel['panel_number']}: {panel['title']}"),ln=True)
        image_path=BASE_DIR/"static"/panel["image"].replace("/static/","")
        if image_path.exists(): pdf.image(str(image_path),x=15,y=30,w=180)
        pdf.set_y(145); pdf.set_font("Arial","",11); pdf.multi_cell(0,7,clean_text(panel["scene_description"])); pdf.ln(3); pdf.multi_cell(0,7,clean_text("Caption: "+panel["caption"])); pdf.ln(2); pdf.multi_cell(0,7,clean_text("Narration: "+panel["narration"]))
    pdf.output(str(path)); return f"/download/{filename}"
