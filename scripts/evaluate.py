import os
import sys
import hashlib
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import load_env, init_db, request_ai_engine

def evaluate_content(limit):
    load_env()
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT url FROM entries WHERE topic_depth_grade IS NULL")
    targets = cursor.fetchall()
    if limit:
        targets = targets[:limit]

    for (url,) in targets:
        safe_filename = hashlib.md5(url.encode()).hexdigest() + ".txt"
        filepath = os.path.join("data/scratch", safe_filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            page_text = f.read()[:4000]

        prompt = f"""
        Analyze this web page text for content density and semantic clarity:
        ---
        {page_text}
        ---
        Grade metrics explicitly mapped:
        - topic_depth_grade: 1.0 (shallow surface level) to 10.0 (master enterprise asset coverage)
        - entity_alignment_score: 1.0 (unstructured text) to 10.0 (precise entities)

        Return your validation arrays strictly as JSON keys without markdown block modifications:
        {{"topic_depth_grade": <value>, "entity_alignment_score": <value>}}
        """

        print(f" Evaluating semantic attributes for: {url}")
        res = request_ai_engine(prompt)
        if res and "topic_depth_grade" in res and "entity_alignment_score" in res:
            depth = max(1.0, min(10.0, float(res["topic_depth_grade"])))
            align = max(1.0, min(10.0, float(res["entity_alignment_score"])))
            
            cursor.execute("""
                UPDATE entries 
                SET topic_depth_grade = ?, entity_alignment_score = ? 
                WHERE url = ?
            """, (depth, align, url))
            conn.commit()
            print(f"   -> Assigned Ratings -> Depth: {depth} | Alignment: {align}")

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standalone Intelligence Auditing Node")
    parser.add_argument("-l", "--limit", type=int, default=None, help="Cap processing counts.")
    args = parser.parse_args()
    evaluate_content(args.limit)
