def build_comic_layout(outline, story, images):
    return [{"panel_number": outline[i]["panel_number"], "title": outline[i]["title"], "scene_description": outline[i]["scene_description"], "image_prompt": outline[i]["image_prompt"], "image": images[i], "caption": story[i]["caption"], "narration": story[i]["narration"]} for i in range(5)]
