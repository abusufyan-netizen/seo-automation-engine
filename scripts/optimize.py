import os
import sys
import json
import hashlib
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import load_env, init_db, request_ai_engine

def generate_schema(threshold):
    load_env()
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT url FROM entries 
        WHERE entity_alignment_score >= ? AND generated_jsonld IS NULL
    """, (threshold,))
    targets = cursor.fetchall()

    for (url,) in targets:
        safe_filename = hashlib.md5(url.encode()).hexdigest() + ".txt"
        filepath = os.path.join("data/scratch", safe_filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            page_text = f.read()[:2000]

        prompt = f"""
        Based on this raw page copy slice, extract key concepts and compile a single structured, minified Schema.org JSON-LD graph.
        Target Location URL: {url}
        ---
        {page_text}
        ---
        The output must be a valid @context JSON object representing a WebPage entity containing key entities or semantic descriptions. Return only the raw minified JSON string. No markdown formatting.
        """

        print(f"📦 Compiling structured entity graph manifests for: {url}")
        res = request_ai_engine(prompt)
        if res:
            json_str = json.dumps(res)
            cursor.execute("""
                UPDATE entries SET generated_jsonld = ? WHERE url = ?
            """, (json_str, url))
            conn.commit()
            print(f"   ✅ JSON-LD schema compiled and stored.")

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standalone Semantic Schema Generation Node")
    parser.add_argument("-t", "--threshold", type=float, default=6.0, help="Minimum entity alignment filter baseline threshold score.")
    args = parser.parse_args()
    generate_schema(args.threshold)
