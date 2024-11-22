# Morningstar Metrics Scraper

A Python-based web scraper designed to collect financial metrics from Morningstar and calculate key financial ratios. This tool automates the process of gathering stock data and computing important metrics for investment analysis.

## Calculated Metrics

The scraper calculates three key financial metrics:

1. 目標殖利率 (Target Yield Rate)
   ```
   Target Yield = Dividend Per Share / (Current Price * 1.2)
   ```

2. 相對 P/B (Relative Price-to-Book)
   ```
   Relative P/B = Price-to-Book Ratio * Book Value
   ```

3. PEG 成長股 (PEG Growth)
   ```
   PEG Growth = (P/E Ratio * Growth Rate) * 100
   ```

## Project Structure

```
morningstar-metrics-scraper/
├── .gitignore                # Git ignore file
├── LICENSE                   # MIT License
├── README.md                # Project documentation
├── requirements.txt         # Project dependencies
├── main.py                  # Main execution script
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── scraper.py          # Main scraping logic
│   ├── utils.py            # Utility functions
│   └── logger.py           # Logging configuration
├── data/
│   ├── input/
│   │   └── tickers.csv     # Input file with stock tickers
│   └── output/
│       └── .gitkeep        # Keep empty output directory
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py
│   └── test_utils.py
└── venv/                    # Virtual environment (not in git)
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

### For macOS

1. Install Homebrew (if not installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python:
```bash
brew install python
```

3. Clone the repository:
```bash
git clone https://github.com/yourusername/morningstar-metrics-scraper.git
cd morningstar-metrics-scraper
```

4. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### For Windows

1. Clone the repository:
```bash
git clone https://github.com/ceteongvanness/morningstar-metrics-scraper.git
cd morningstar-metrics-scraper
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

After activating the virtual environment:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create input data file (data/input/tickers.csv):
```csv
Ticker
AAPL
MSFT
GOOGL
META
AMZN
```

2. Environment variables can be set in `.env` file:
```env
LOG_LEVEL=INFO
DEFAULT_DELAY=2
MAX_RETRIES=3
```

## Usage

1. Basic usage:
```bash
python main.py
```

2. With custom input/output:
```bash
python main.py --input data/input/my_tickers.csv --output data/output/results.csv
```

3. With custom delay:
```bash
python main.py --delay 3
```

## Output Format

The scraper generates a CSV file with the following columns:

```csv
ticker,timestamp,dividend_per_share,current_price,pb_ratio,pe_ratio,growth_rate,target_yield_rate,relative_pb,peg_growth,error
AAPL,2024-11-22 10:30:15,0.92,175.50,45.2,28.5,12.3,0.00437,23.45,556.0,
```

## Error Handling

The scraper includes comprehensive error handling:
- Automatic retry for failed requests
- Rate limit handling
- Connection error recovery
- Data validation
- Detailed logging

## Troubleshooting

1. Python Not Found:
```bash
# For macOS
brew install python

# Verify installation
python3 --version
```

2. Package Installation Issues:
```bash
# Upgrade pip
pip install --upgrade pip

# Install packages individually
pip install pandas
pip install requests
pip install beautifulsoup4
```

3. Permission Issues:
```bash
# If you get permission errors
sudo pip install -r requirements.txt
```

## Development

1. Running tests:
```bash
python -m pytest tests/
```

2. Check code style:
```bash
flake8 src/
```

3. Format code:
```bash
black src/
```

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes:
```bash
git commit -m 'Add some AmazingFeature'
```
4. Push to the branch:
```bash
git push origin feature/AmazingFeature
```
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes only. Please review and comply with Morningstar's terms of service before use. Ensure you have the right to access and use the data you're collecting.

## Acknowledgments

- Beautiful Soup documentation
- Requests library documentation
- Pandas documentation

## Version History

- 1.0.0
  - Initial Release
  - Basic scraping functionality
  - Three key financial metrics calculation