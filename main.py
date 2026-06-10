import os
import time
import argparse
from scripts.utils import load_env, init_db
from scripts.crawl import execute_crawl
from scripts.evaluate import evaluate_content
from scripts.optimize import generate_schema

def run_pipeline_cycle(target_urls, alignment_threshold):
    print("\n⚡ --- Starting Autonomous Optimization Pipeline Loop --- ⚡")
    init_db()
    
    # Execution Pass 1: Crawl targets sequentially
    for url in target_urls:
        if url.strip():
            execute_crawl(url.strip())
            
    # Execution Pass 2: Process evaluations locally via Ollama
    evaluate_content(limit=None)
    
    # Execution Pass 3: Convert structured insights into component micro-data
    generate_schema(alignment_threshold)
    print("🏁 --- Optimization processing run execution wave complete --- 🏁\n")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Technical SEO Entity Mining & Crawl Architecture")
    parser.add_argument("-u", "--urls", help="Comma-separated target addresses block updates.")
    parser.add_argument("-t", "--threshold", type=float, default=6.0, help="Lower-bound verification limit scale metrics scores.")
    parser.add_argument("-i", "--infinite", action="store_true", help="Lock orchestration threads inside structural loops.")
    parser.add_argument("--sleep", type=int, default=1800, help="Loop iteration sleep interval frames (seconds).")
    
    args = parser.parse_args()
    load_env()

    # Default lookup seed targets if explicitly absent from arguments array options
    target_list = args.urls.split(",") if args.urls else ["https://example.com"]

    if args.infinite:
        print(f"🔁 Running engine diagnostics inside continuous loops. Frequency spacing interval: {args.sleep}s")
        try:
            while True:
                run_pipeline_cycle(target_list, args.threshold)
                time.sleep(args.sleep)
        except KeyboardInterrupt:
            print("\n🛑 Pipeline engine loop execution commands exited gracefully via command interrupt signals.")
    else:
        run_pipeline_cycle(target_list, args.threshold)

if __name__ == "__main__":
    main()
