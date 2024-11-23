# Stock Analysis Tool

A Python-based tool for scraping financial metrics from Morningstar and calculating stock valuations using different methodologies.

## Features

- Scrapes key financial metrics from Morningstar
- Calculates three different valuation methods:
  - Target Yield Valuation (目標殖利率估價法)
  - Relative P/B Valuation (相對P/B估價法)
  - PEG Growth Valuation (PEG成長股估價法)
- Exports results in CSV format with Chinese column headers
- Includes rate limiting and error handling
- Comprehensive logging system

## Generated Metrics

The tool collects and calculates the following metrics:
- 股票代碼 (Stock Code)
- 現在股價 (Current Price)
- 目標殖利率 估價法 (Target Yield Valuation)
- 相對 P/B 估價法 (Relative P/B Valuation)
- PEG 成長股 估價法 (PEG Growth Valuation)
- 該公司 股息(TTM) (Company Dividend TTM)
- 該公司近5年 平均殖利率 (5-Year Average Yield)
- 該公司 BVPS(TTM) (Company BVPS TTM)
- 該公司近5年 平均P/B (5-Year Average P/B)
- 該公司 EPS(TTM) (Company EPS TTM)
- 該公司 EPS成長率％ (Company EPS Growth Rate%)

## Project Structure

```
stock-analysis-tool/
├── src/
│   ├── constants/         # Configuration and constants
│   ├── scrapers/         # Web scraping modules
│   ├── models/           # Data models
│   ├── utils/            # Utility functions
│   └── formatters/       # Output formatting
├── data/
│   ├── input/           # Input files
│   └── output/          # Generated results
├── logs/                # Log files
└── tests/              # Unit tests
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### For MacOS

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

5. Install dependencies:
```bash
pip install -r requirements.txt
```

### For Windows

1. Clone the repository:
```bash
git clone https://github.com/ceteongvanness/stock-analysis-tool.git
cd stock-analysis-tool
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your input file (data/input/tickers.csv):
```csv
Ticker
AAPL
MSFT
GOOGL
```

2. Run the scraper:
```bash
# Basic usage
python main.py --input data/input/tickers.csv

# Specify output file
python main.py --input data/input/tickers.csv --output data/output/results.csv
```

The script will generate a timestamped CSV file with the following format:
```csv
股票代碼,現在股價,目標殖利率 估價法,相對 P/B 估價法,PEG 成長股 估價法,該公司 股息(TTM),該公司近5年 平均殖利率,該公司 BVPS(TTM),該公司近5年 平均P/B,該公司 EPS(TTM),該公司 EPS成長率％
AAPL,175.50,69.44,450.00,1500.00,0.92,3.00,100.00,4.50,15.00,15.00
```

## Calculations

1. Target Yield Valuation:
```python
target_yield = dividend_ttm / (yield_5yr_avg * 1.2)
```

2. Relative P/B Valuation:
```python
relative_pb = bvps_ttm * pb_5yr_avg
```

3. PEG Growth Valuation:
```python
peg_valuation = eps_ttm * eps_growth * 100
```

## Error Handling

The scraper includes:
- Automatic retry for failed requests
- Rate limiting to prevent blocking
- Data validation
- Comprehensive error logging
- Default values for missing data

## Common Issues

1. ModuleNotFoundError:
```bash
pip install -r requirements.txt
```

2. Permission Issues:
```bash
chmod +x main.py
```

3. Encoding Issues:
```python
# UTF-8-BOM encoding is used for proper Chinese character display
df.to_csv('output.csv', encoding='utf-8-sig')
```

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes:
```bash
git commit -m 'Add AmazingFeature'
```
4. Push to the branch:
```bash
git push origin feature/AmazingFeature
```
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes only. Users should verify the accuracy of the data and perform their own due diligence before making any investment decisions.

## Acknowledgments

- Beautiful Soup documentation
- Pandas documentation
- Requests library documentation
- Morningstar for providing financial data

## Version History

- 1.0.0
  - Initial Release
  - Basic scraping functionality
  - Three valuation methods
  - CSV output with Chinese headers