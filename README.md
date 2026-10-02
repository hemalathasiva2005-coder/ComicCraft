# ComicCraft New

```powershell
cd C:\NM\ComicCraft_New
..\env\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own Gemini and Hugging Face keys.

```powershell
..\env\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs
