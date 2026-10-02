from pydantic import BaseModel, Field
class PanelOutline(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
class StoryPanel(BaseModel):
    panel_number: int
    title: str
    caption: str
    narration: str
class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3)
    character_name: str
    setting: str
    tone: str
    art_style: str
