import os
import sys
import hashlib
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import load_env, init_db, request_ai_engine

def analyze_entity_gap(target_url, competitor_url):
    load_env()
    target_file = os.path.join("data/scratch", hashlib.md5(target_url.encode()).hexdigest() + ".txt")
    competitor_file = os.path.join("data/scratch", hashlib.md5(competitor_url.encode()).hexdigest() + ".txt")

    if not os.path.exists(target_file) or not os.path.exists(competitor_file):
        print("❌ Error: One or both URLs have not been crawled yet.")
        print("💡 Please run main.py or scripts/crawl.py for both URLs first to populate the cache.")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        target_text = f.read()[:3000]
    with open(competitor_file, "r", encoding="utf-8") as f:
        competitor_text = f.read()[:3000]

    prompt = f"""
    You are an elite semantic SEO strategist and entity optimization engine.
    Compare the following two web page content text slices:

    TARGET TEXT (Our Page):
    ---
    {target_text}
    ---

    COMPETITOR TEXT (Ranked Higher):
    ---
    {competitor_text}
    ---

    Identify exactly 3 to 5 vital technical entities, thematic concepts, or subtopics that are prominently present in the COMPETITOR TEXT but are completely absent or severely lacking in the TARGET TEXT.
    
    Provide your response strictly as a valid, structured JSON object matching this schema without any markdown blocks or conversational text wrapping:
    {{
        "target_url": "{target_url}",
        "competitor_url": "{competitor_url}",
        "missing_entities": [
            {{"entity": "Term/Concept Name", "reason": "Why this entity matters for thematic depth and content coverage."}}
        ],
        "strategic_recommendation": "One sentence actionable copy directive."
    }}
    """

    print(f"🤖 Processing local AI Entity Gap Analysis...")
    print(f"   ↳ Target:     {target_url}")
    print(f"   ↳ Competitor: {competitor_url}")
    
    res = request_ai_engine(prompt)
    if res:
        print("\n📊 --- Competitive Intelligence Insights ---")
        import json
        print(json.dumps(res, indent=2))
        return res
    else:
        print("❌ Gap analysis engine execution wave encountered an model evaluation bypass.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Competitive Entity Gap Detector")
    parser.add_argument("-t", "--target", required=True, help="Your target URL address.")
    parser.add_argument("-c", "--competitor", required=True, help="The competitor URL address to audit against.")
    args = parser.parse_args()
    analyze_entity_gap(args.target, args.competitor)
