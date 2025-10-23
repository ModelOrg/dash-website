# Sports Analytics Platform

A collaborative sports analytics website for exploring NFL data with your friends. Built with Dash for easy Python-only development.

## 🚀 Quick Start

```bash
# 1. Clone and navigate to the repo
cd dash-website

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pre-commit install

# 4. Load NFL data (takes ~2-5 minutes)
python utils/load_nfl_data.py

# 5. Run the app
python app.py
```

Visit **http://localhost:8050**

## 📁 Project Structure

```
sports-analytics-platform/
├── data/parquet/              # Parquet data files (gitignored)
├── pages/                     # Folder for analytics pages
│   ├── _template.py           # Template for new dashboards
│   ├── fantasy_value.py       # View stats for specific players
│   ├── home.py                # Landing page
|   └── team_offense_trends.py # View week-by-week totals for each offense
├── utils/                     # Helper functions
│   ├── load_nfl_data.py       # Load NFL data from nflreadpy
│   └── query_engine.py        # Query Parquet files with DuckDB
├── app.py                     # Main Dash application
└── requirements.txt           # Python dependencies
```

## 📚 Documentation

- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - How to add new pages
- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - Building dashboards and using components
- **[DATA_GUIDE.md](docs/DATA_GUIDE.md)** - Available datasets and how to query them

## 🎯 Workflow

1. Create a dev branch: `git checkout -b my-new-analysis`
2. Add your page (copy `pages/_template.py`)
3. Test locally: `python app.py`
4. Make a pull request: [Pull requests](https://github.com/ModelOrg/dash-website/pulls)
5. Once reviewed, merge into main!

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