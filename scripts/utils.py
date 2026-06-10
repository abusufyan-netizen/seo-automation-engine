import os
import json
import sqlite3
import urllib.request

DB_PATH = os.path.join("data", "seo_strategy.sqlite")

def load_env():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            url TEXT PRIMARY KEY,
            content_hash TEXT,
            word_count INTEGER,
            topic_depth_grade REAL,
            entity_alignment_score REAL,
            generated_jsonld TEXT
        )
    """)
    conn.commit()
    return conn

def request_ai_engine(prompt):
    """
    Hybrid AI Gateway: Falls back to Gemini API automatically 
    if local Ollama is absent or non-responsive.
    """
    load_env()
    ollama_url = os.getenv("OLLAMA_URL")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    # ── PATH A: TRY LOCAL OLLAMA FIRST ──
    if ollama_url:
        model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
        payload = {"model": model, "prompt": prompt, "stream": False, "format": "json"}
        headers = {"Content-Type": "application/json"}
        try:
            req = urllib.request.Request(f"{ollama_url}/api/generate", data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=5) as res:
                raw = json.loads(res.read().decode("utf-8"))
                return json.loads(raw["response"].strip())
        except Exception:
            print("ℹ️ Local Ollama endpoint offline or missing. Switching to public cloud fallback pipeline...")

    # ── PATH B: FREE TIER CLOUD FALLBACK (GEMINI) ──
    if gemini_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        headers = {"Content-Type": "application/json"}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as res:
                raw = json.loads(res.read().decode("utf-8"))
                text_response = raw["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text_response.strip())
        except Exception as e:
            print(f"❌ Cloud execution matrix failure: {e}")
            return None

    print("❌ Critical System Fault: Neither OLLAMA_URL nor GEMINI_API_KEY could be resolved inside parameters.")
    return None
