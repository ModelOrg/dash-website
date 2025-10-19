7. Development Workflow
7.1 Setup for New Contributors
Prerequisites:

Python 3.10+
R (if working with nflverse)
Git

Initial Setup:
bash# Clone repository
git clone <repo-url>
cd sports-analytics-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run the app
python app.py
Visit: http://localhost:8050
7.2 Adding a New Page

Copy pages/_template.py to pages/my_analysis.py
Update page registration:

python   dash.register_page(__name__, path="/my-analysis", name="My Analysis")

Build your layout and callbacks
Refresh browser - page appears in navbar automatically!

7.3 Adding New Data

Add data to data/parquet/my_data.parquet
Document in docs/DATA_GUIDE.md
Query using DuckDB:

python   df = query_parquet("SELECT * FROM 'my_data.parquet'")


11. Security & Best Practices
11.1 Environment Variables (.env)
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sports_db

# API Keys (if needed)
SPORTS_API_KEY=your_key_here

# R Service
R_API_URL=http://localhost:8000

# Deployment
ENV=development  # or production
DEBUG=True
Never commit .env to Git!
11.2 Access Control (Future)
For now, this is internal-only. Future considerations:

Add Dash authentication for user accounts
Role-based access to pages
API key authentication for FastAPI


12. Monitoring & Debugging
12.1 Logging
pythonimport logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Page loaded successfully")
12.2 Error Handling in Callbacks
python@callback(...)
def my_callback(value):
    try:
        # Your logic
        return result
    except Exception as e:
        logger.error(f"Error in callback: {e}")
        return html.Div("An error occurred. Check logs.")