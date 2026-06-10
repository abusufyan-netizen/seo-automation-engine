
# 🕸️ Autonomous Content Strategy & Entity Scraping Engine

### A Browserless, Hybrid Intelligence Loop for Strategic SEO Auditing, Gap Detection & JSON-LD Generation

An elite growth-engineering utility designed to crawl web assets, execute semantic thematic analysis, map competitive entity gaps, and automatically compile minified JSON-LD micro-data structures.

Built entirely using the **Python Standard Library**—delivering maximum execution speed and absolute data control with a completely empty `requirements.txt`.

---

## 🔀 Hybrid Intelligence Core (Dual-Engine Execution)

To eliminate deployment friction and hardware barriers, this framework features an adaptive dual-engine processing pipeline:

* **Decentralized Offline Track:** Processes text sets completely air-gapped on your local hardware using an **Ollama** daemon node (`qwen2.5-coder:7b`).
* **Zero-Setup Cloud Track:** Seamlessly switches to a secure, direct standard-library HTTP connection to **Gemini's free tier API** (`gemini-2.5-flash`) if local systems are absent. No complex packages or SDK installations required.

---

## 🔮 Core Architecture Capabilities

* **Browserless Text Extraction:** Rapid raw HTML ingestion via native `urllib` pipelines, utilizing low-overhead regex to strip bloated inline layout tags, script nodes, and styling layers.
* **Local & Cloud Semantic Auditing:** Evaluates webpage text for structural thematic coverage, text density, and keyword depth based on strict target compliance scales.
* **Competitive Entity Gap Analysis:** Compares cached text strings from your page against top-ranking competitor assets to surface missing semantic clusters and actionable copy directives.
* **Automatic Micro-data Compiling:** Generates valid, minified Schema.org JSON-LD graph objects (`WebPage` graphs) for assets clearing your custom quality constraints.
* **Zero-Dependency Serverless Storage:** Leverages a lightweight, transactional local SQLite storage matrix (`/data`) requiring zero external database hosting servers.

---

## 🛠️ The Local Data Pipeline

```text
[ Target Ingestion ] ──> [ Browserless Ingestion ] ──> [ SQLite Cash Matrix ]
                                                                │
[ Minified JSON-LD ] <── [ Threshold Passed? (Yes) ] <── [ Hybrid AI Engine ]
                                                             (Ollama / Gemini)

```

1. **Ingest & Clean (`crawl.py`):** Fetches the web asset, strips tracking/layout script noise, and caches clean text to disk using an encrypted MD5 hash.
2. **Semantic Audit (`evaluate.py`):** Passes cached frames to your chosen model to assign independent metric grades (`topic_depth_grade` and `entity_alignment_score`).
3. **Structured Compilation (`optimize.py`):** Converts audited content insight profiles into injection-ready Schema.org JSON-LD components.

---

## ⚙️ Project Folder Blueprint

```text
.
├── data/                       # Automatically created on first runtime pass
│   ├── scratch/                # Holds temporary cached clean text files
│   └── seo_strategy.sqlite     # Standalone file-based SQLite database
├── scripts/                    # Independent processing scripts package
│   ├── __init__.py             # Empty init package pointer
│   ├── crawl.py                # Ingestion & HTML regex cleaning node
│   ├── evaluate.py             # Hybrid AI semantic auditing node
│   ├── gap_analysis.py         # Competitive entity gap intelligence agent
│   ├── optimize.py             # Schema.org component compiler node
│   └── utils.py                # Shared database core & routing gateway
├── .env                        # Private execution variables (Git ignored)
├── .env.example                # Shared ecosystem environment template
├── main.py                     # Master pipeline orchestration wrapper
└── requirements.txt            # Empty (0 third-party packages required)

```

---

## 🚀 Setup & Usage Guide

### 1. Configure Your System Parameters

Create a `.env` file in your project root directory and supply your chosen environment key metrics:

```env
# CHOICE A: Standalone Cloud Performance (Zero Local Setup Overhead)
GEMINI_API_KEY=AIzaSyYourFreeGeminiKeyFromGoogleAIStudio

# CHOICE B: Fully Decentralized Offline Processing (Optional)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b

```

### 2. Trigger a Single Operational Execution Wave

Execute the orchestration pipeline directly by feeding a comma-separated list of target strings to `main.py`:

```bash
python3 main.py --urls "[https://vercel.com](https://vercel.com),[https://github.com](https://github.com)" --threshold 6.5

```

### 3. Loop the Engine Topology Continuously

Lock the diagnostic agent threads into a background polling loop that refreshes at designated intervals (e.g., every 30 minutes / 1800 seconds):

```bash
python3 main.py --urls "[https://example.com](https://example.com)" --threshold 7.0 --infinite --sleep 1800

```

### 4. Run an Autonomous Competitive Entity Gap Audit

Compare your landing page copy directly against a top-ranking competitor asset to map missing semantic schemas completely privately:

```bash
# Step 1: Cache both properties into your SQLite data matrix
python3 main.py --urls "[https://yoursite.com/page,https://competitor.com/best-page](https://yoursite.com/page,https://competitor.com/best-page)"

# Step 2: Trigger the gap verification agent
python3 scripts/gap_analysis.py --target "[https://yoursite.com/page](https://yoursite.com/page)" --competitor "[https://competitor.com/best-page](https://competitor.com/best-page)"

```

---

## 📊 Standard CLI Terminal Reporting Preview

```bash
$ python3 main.py --urls "[https://example.com](https://example.com)" --threshold 7.0

⚡ --- Starting Autonomous Optimization Pipeline Loop --- ⚡
🌐 Crawling target source network frame location: [https://example.com](https://example.com)
   ✅ Target metrics cached. [Words: 642 | Hash: 8b1a9953c4611296a827abf8c47804d7]
🤖 Evaluating semantic attributes for: [https://example.com](https://example.com)
   -> Assigned Ratings -> Depth: 8.5 | Alignment: 7.2
📦 Compiling structured entity graph manifests for: [https://example.com](https://example.com)
   ✅ JSON-LD schema compiled and stored.
🏁 --- Optimization processing run execution wave complete --- 🏁

```

---

### 🤝 Contributing & Updates

If this dependency-free hybrid crawling architecture optimized your search visibility or technical engineering workflows, drop a ⭐ on this repository!

Follow my profile [@abusufyan-netizen](https://github.com/abusufyan-netizen) to stay up-to-date with a steady stream of local automation frameworks and high-performance open-source applications.
