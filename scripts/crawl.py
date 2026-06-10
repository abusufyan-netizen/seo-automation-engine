import os
import sys
import hashlib
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import load_env, init_db

def clean_html_to_text(html_content):
    """Dependency-free text extraction sequence tracking body structures."""
    import re
    # Lowercase tag transformations for uniform matching strings
    html = re.sub(r'<(script|style)[^>]*>([\s\S]*?)<\/\1>', '', html_content, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', html)
    # Clean whitespace strings configurations
    cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(cleaned_lines)

def execute_crawl(target_url):
    load_env()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SEO-Scout-Agent/1.0"}
    req = urllib.request.Request(target_url, headers=headers)
    
    print(f"🌐 Crawling target source network frame location: {target_url}")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_html = response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ Failed network retrieval pass bounds: {e}")
        return

    cleaned_text = clean_html_to_text(raw_html)
    word_count = len(cleaned_text.split())
    content_hash = hashlib.md5(cleaned_text.encode("utf-8")).hexdigest()

    conn = init_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO entries (url, content_hash, word_count)
            VALUES (?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET content_hash=excluded.content_hash, word_count=excluded.word_count
        """, (target_url, content_hash, word_count))
        conn.commit()
        # Cache raw context data temporarily for downstream extraction passes
        os.makedirs("data/scratch", exist_ok=True)
        safe_filename = hashlib.md5(target_url.encode()).hexdigest() + ".txt"
        with open(os.path.join("data/scratch", safe_filename), "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        print(f"   ✅ Target metrics cached. [Words: {word_count} | Hash: {content_hash}]")
    except Exception as e:
        print(f"❌ DB write tracking breakdown error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standalone Browserless Crawl Node")
    parser.add_argument("-u", "--url", required=True, help="Target URL address destination to crawl.")
    args = parser.parse_args()
    execute_crawl(args.url)
