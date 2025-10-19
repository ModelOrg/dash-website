# Sports Analytics Platform

A collaborative sports analytics website for exploring NFL data with your friends. Built with Dash for easy Python-only development.

## 🚀 Quick Start

```bash
# 1. Clone and navigate to the repo
cd sports-analytics-platform

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Load NFL data (takes ~2-5 minutes)
python utils/load_nfl_data.py

# 5. Run the app
python app.py
```

Visit **http://localhost:8050**

## 📁 Project Structure

```
sports-analytics-platform/
├── app.py                    # Main Dash application
├── requirements.txt          # Python dependencies
├── pages/                    # Your analytics pages
│   ├── home.py              # Landing page
│   ├── _template.py         # Template for new pages
│   └── example_nfl.py       # NFL stats dashboard
├── utils/                    # Helper functions
│   ├── query_engine.py      # Query Parquet files with DuckDB
│   └── load_nfl_data.py     # Load NFL data from nflreadpy
└── data/parquet/            # Parquet data files (gitignored)
```

## 📚 Documentation

- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - How to add new pages
- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - Building dashboards and using components
- **[DATA_GUIDE.md](docs/DATA_GUIDE.md)** - Available datasets and how to query them

## 🎯 Workflow

1. Create a dev branch: `git checkout -b my-new-analysis`
2. Add your page (copy `pages/_template.py`)
3. Test locally: `python app.py`
4. Commit and merge to main when ready
5. Page automatically appears in navigation!

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed instructions on adding pages.

## 💾 Data Updates

Refresh NFL data anytime:
```bash
python utils/load_nfl_data.py
```

## 🛠️ Tech Stack

- **Dash** - Web framework (Python only!)
- **DuckDB** - Fast queries on Parquet files
- **Plotly** - Interactive visualizations
- **nflreadpy** - NFL data source

---

**Questions?** Check the docs or ask the team!