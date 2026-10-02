import re, time
from pathlib import Path
from PIL import Image, ImageDraw
from huggingface_hub import InferenceClient
from app.config import HF_TOKEN, HF_IMAGE_MODEL, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_STEPS, validate_required_keys
BASE_DIR=Path(__file__).resolve().parent.parent
PANEL_DIR=BASE_DIR/"static"/"panels"
PANEL_DIR.mkdir(parents=True, exist_ok=True)
def safe_name(text): return re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")[:50] or "panel"
def placeholder(panel_number,error):
    filename=f"panel_{panel_number}_{int(time.time())}.png"; path=PANEL_DIR/filename
    image=Image.new("RGB",(IMAGE_WIDTH,IMAGE_HEIGHT),"white"); draw=ImageDraw.Draw(image)
    draw.rectangle((10,10,IMAGE_WIDTH-10,IMAGE_HEIGHT-10),outline="black",width=4)
    draw.text((30,40),f"Panel {panel_number} - Image generation unavailable",fill="black")
    draw.text((30,80),str(error)[:220],fill="black"); image.save(path); return path
def generate_image(image_prompt,panel_number,art_style):
    validate_required_keys(require_images=True)
    prompt=f"""{image_prompt}\nVisual style: {art_style}\nCinematic comic-book illustration, expressive characters, consistent character appearance, clear composition, detailed environment, no text, no speech bubbles, no watermark, no logo."""
    try:
        image=InferenceClient(api_key=HF_TOKEN,provider="auto").text_to_image(prompt=prompt,model=HF_IMAGE_MODEL,width=IMAGE_WIDTH,height=IMAGE_HEIGHT,num_inference_steps=IMAGE_STEPS,negative_prompt="blurry, distorted face, extra fingers, watermark, text, logo")
        filename=f"panel_{panel_number}_{safe_name(art_style)}_{int(time.time())}.png"; path=PANEL_DIR/filename; image.save(path)
        return f"/static/panels/{filename}"
    except Exception as exc:
        path=placeholder(panel_number,exc); return f"/static/panels/{path.name}"
