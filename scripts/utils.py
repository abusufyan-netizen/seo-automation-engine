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

def request_ollama(prompt, url, model):
    payload = {"model": model, "prompt": prompt, "stream": False, "format": "json"}
    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(f"{url}/api/generate", data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req) as res:
            raw = json.loads(res.read().decode("utf-8"))
            return json.loads(raw["response"].strip())
    except Exception as e:
        print(f"⚠️ Ollama parse extraction failed: {e}")
        return None
