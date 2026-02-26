# hasya-llm

AI system that generates **original Hindi stand-up comedy scripts** by learning style from real stand-up (RAG over humor patterns, not factual QA).

## Pipeline

1. **Ingestion**: YouTube URL → audio (yt-dlp) → transcription (Whisper) → joke segmentation (LLM) → metadata extraction → stored joke units  
2. **Vector store**: Each joke is embedded and stored in Supabase (pgvector).  
3. **Generation**: User topic → retrieve similar joke *patterns* → LLM generates a new 5‑minute script (no copying).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY
```

## Run API

```bash
uvicorn app.main:app --reload
```

## Project layout

- `app/api/` — FastAPI routes  
- `app/core/` — config, shared types  
- `app/ingestion/` — YouTube → transcripts → jokes  
- `app/generation/` — retrieval + script generation  
- `data/` — raw_audio, raw_transcripts, processed_jokes, scripts  

## Config

All configuration is via `.env` (see `.env.example`). No hardcoded secrets.
