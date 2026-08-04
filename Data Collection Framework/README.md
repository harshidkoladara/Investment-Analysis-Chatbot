# Data Collection Framework

A robust, modular Python framework designed to collect, parse, and structure investment analysis data from multiple public and premium sources. It compiles news, SEC corporate filings, RSS feeds, and social sentiment into standard structured data formats.

---

## Architecture and Design

The framework is built around a unified base client to guarantee consistent timeouts, automated retries, and proxy rotations.

```
├── main.py                          # CLI Execution entry point
├── Dockerfile                       # Standard runtime container configuration
├── docker-compose.yml               # Multi-service setup (App + MongoDB database)
├── requirements.txt                 # Project dependencies
├── utils/                           # Core utilities
│   ├── base.py                      # Base Downloader HTTP Client
│   └── get_proxy.py                 # Free Proxy Scraper and IP Checker
├── news/                            # Company News downloader (Finnhub API)
│   ├── base.py
│   └── collect_news.py
├── news_rss/                        # RSS XML parser (CNBC, etc.)
│   ├── base.py
│   └── collect_rss.py
├── announcements/                   # SEC EDGAR announcement scraper
│   ├── base.py
│   └── collect_announcements.py
└── socialmedia/                     # Sentiment scraper (Twitter/X - legacy)
    ├── base.py
    └── collect_twitter.py
```

### Module Design:
1. **`BaseDownloader`**: Implements custom connection configurations, retries, and dynamic headers.
2. **`CollectRSSNews`**: Downloads and parses real-time XML RSS feeds using `lxml` XPath queries.
3. **`CollectNews`**: Fetches stock company news from the Finnhub API and crawls the original article content ( Fool, Yahoo Finance, Reuters, MarketWatch, CNBC, etc.).
4. **`CollectAnnouncements`**: Searches the SEC EDGAR endpoint using stock tickers, resolves the Central Index Key (CIK), and extracts full text from forms.
5. **`CollectTwitter`**: Legacy tracker for Twitter sentiment (Deprecated).

---

## Technologies
* **Language**: Python 3.11
* **Parsing**: `lxml` (XPath), `parsel`
* **Data Handling**: `pandas`, `tqdm`
* **Network**: `requests`, `pyOpenSSL`

---

## Installation & Setup

### Configuration
1. Copy the `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Configure variables in the `.env` file (e.g., set `FINNHUB_API_KEY`).

### Local Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Docker Setup
To spin up the python service along with a MongoDB database instance:
```bash
docker-compose up --build -d
```

---

## Usage

Use the command line interface to run different data collection sources.

```bash
# Run the RSS feed downloader (Default)
python3 main.py --source rss

# Run the Company News downloader (requires FINNHUB_API_KEY in .env)
python3 main.py --source news

# Run the SEC Announcements downloader
python3 main.py --source sec
```

---

## Future Improvements
* Complete OAuth support for Twitter/X API integration.
* Add MongoDB saving handlers within `main.py` pipelines.
