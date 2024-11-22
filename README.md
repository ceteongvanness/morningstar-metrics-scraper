# Morningstar Metrics Scraper

A Python-based web scraper for collecting financial metrics and fundamental data from Morningstar. This tool automatically fetches data such as dividend yields, P/B ratios, and other key financial metrics for multiple stock tickers.

## Features

- Bulk data scraping for multiple stock tickers
- CSV input/output support
- Rate limiting to prevent server blocking
- Error handling and retry mechanisms
- Detailed logging
- Progress tracking
- Periodic data saving to prevent data loss

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ceteongvanness/morningstar-metrics-scraper.git
cd morningstar-metrics-scraper
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your input file:
   - Create a CSV file in the `data/input` directory
   - Format: single column with header 'Ticker'
   - Example:
     ```csv
     Ticker
     AAPL
     MSFT
     GOOGL
     ```

2. Run the scraper:
```bash
python main.py --input data/input/tickers.csv --output data/output/results.csv
```

### Command Line Arguments

- `--input`: Path to input CSV file (default: data/input/tickers.csv)
- `--output`: Path to output CSV file (optional)

## Output Data

The scraper collects the following metrics for each ticker:
- Dividend Per Share (TTM)
- Price to Book Ratio
- PE Ratio
- [Add other metrics you're collecting]

Sample output format:
```csv
ticker,dividend,pb_ratio,pe_ratio,status
AAPL,0.92,45.2,28.5,success
MSFT,2.48,15.6,35.2,success
```

## Project Structure

```
morningstar-metrics-scraper/
├── data/
│   ├── input/          # Input CSV files
│   └── output/         # Scraped data output
├── src/
│   ├── scraper.py      # Main scraping logic
│   ├── utils.py        # Utility functions
│   └── logger.py       # Logging configuration
├── tests/              # Unit tests
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Configuration

Key settings can be modified in `src/config.py`:
- Request delay time
- User agent settings
- Base URLs
- Retry attempts
- [Other configurable parameters]

## Error Handling

The scraper includes:
- Automatic retry for failed requests
- Rate limit handling
- Connection error recovery
- Data validation
- Detailed error logging

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes only. Please review and comply with Morningstar's terms of service before use. Ensure you have the right to access and use the data you're collecting.

## Acknowledgments

- Beautiful Soup documentation
- Requests library documentation