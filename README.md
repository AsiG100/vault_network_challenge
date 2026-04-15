# Vault Exercise

This project scrapes an affiliate performance table from the provided QuickSight dashboard, validates and normalizes the rows, and exports the result to `output.json` in the repository root.

## What It Does

- Logs into the dashboard with Playwright
- Exports the table data to a temporary CSV
- Normalizes and validates each row with Pydantic
- Writes the final JSON payload to `output.json`

## Requirements

- Python 3.11+ recommended
- Access to the QuickSight dashboard
- A `.env` file with dashboard credentials

Dashboard URL:

`https://us-east-1.quicksight.aws.amazon.com/sn/account/vault-network-inteview/dashboards/3b1cdcb4-3d00-4612-9ff3-4940982b2e99`

## Output Format

Each record in `output.json` contains:

- `date`: formatted as `YYYY-MM-DD`
- `code`: must start with `AFF`
- `registration`: integer
- `ftds`: integer
- `state`: valid two-letter US state abbreviation

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:

```bash
playwright install chromium
```

4. Create a `.env` file in the project root with:

```env
DASHBOARD_URL=https://us-east-1.quicksight.aws.amazon.com/sn/account/vault-network-inteview/dashboards/3b1cdcb4-3d00-4612-9ff3-4940982b2e99
USERNAME=your_username
PASSWORD=your_password
```

## Run

Execute the main script:

```bash
python main.py
```

When the run succeeds, the script creates `output.json` in the project root.

## Project Structure

- `main.py`: entrypoint, validation, and export flow
- `utils/scraper.py`: dashboard login and table extraction
- `utils/tools.py`: CSV reading, date formatting, and JSON export
- `utils/consts.py`: state code whitelist

## Notes

- The scraper saves a temporary `performance.csv` file during extraction.
- If the dashboard layout or selectors change, the scraping step may need updates.
- Validation failures will stop the run before invalid data is written to `output.json`.
