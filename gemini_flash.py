import json
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, GEMINI_OUTLINE_MODEL, GEMINI_STORY_MODEL, validate_required_keys
from app.schemas import PanelOutline, StoryPanel
def get_client():
    validate_required_keys()
    return genai.Client(api_key=GEMINI_API_KEY)
def generate_outline(story_prompt, character_name, setting, tone, art_style):
    client=get_client()
    prompt=f'''Create a complete 5-panel comic outline.
Story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
Return exactly 5 panels. Keep the same main character throughout. Each panel must have a short title, clear scene description, and detailed image prompt. Do not put text or speech bubbles inside image prompts.'''
    response=client.models.generate_content(model=GEMINI_OUTLINE_MODEL, contents=prompt, config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=list[PanelOutline], max_output_tokens=4000))
    data=json.loads(response.text)
    if len(data)!=5: raise RuntimeError(f"Gemini returned {len(data)} panels instead of 5.")
    return data
def generate_story(outline, character_name, tone):
    client=get_client()
    prompt=f'''Create narration and dialogue for a 5-panel comic.
Main character: {character_name}
Tone: {tone}
Panel outline:
{json.dumps(outline, indent=2, ensure_ascii=False)}
Return exactly 5 story panels. Match panel numbers. Give each a short title, caption, and engaging narration/dialogue. Keep the story consistent.'''
    response=client.models.generate_content(model=GEMINI_STORY_MODEL, contents=prompt, config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=list[StoryPanel], max_output_tokens=5000))
    data=json.loads(response.text)
    if len(data)!=5: raise RuntimeError(f"Gemini returned {len(data)} story panels.")
    return data
