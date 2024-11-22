# Stock Analysis Tool

A financial analysis tool that supports fundamental analysis and scoring systems for regular stocks, bank stocks, and REITs. This tool automatically calculates various financial metrics, generates scores, and provides valuation analysis.

## Features

- Support for three types of stock analysis:
  - Regular stocks
  - Bank stocks
  - REITs
- Automatic financial metrics calculation
- Competitive advantage (Moat) scoring
- Risk assessment
- Multiple valuation methods
- CSV output format

## Requirements

- Python 3.8+
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
git clone https://github.com/ceteongvanness/stock-analysis-tool.git
cd stock-analysis-tool
```

4. Create virtual environment:
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

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
stock-analysis-tool/
├── data/
│   ├── input/           # Input data files
│   │   └── tickers.csv
│   └── output/          # Analysis results
├── src/
│   ├── __init__.py
│   ├── config.py        # Configuration settings
│   ├── scraper.py       # Data scraping
│   ├── normal_scorer.py # Regular stock scoring
│   ├── bank_scorer.py   # Bank stock scoring
│   ├── reit_scorer.py   # REITs scoring
│   └── output_formatter.py # Output formatting
├── tests/
├── requirements.txt
└── main.py
```

## Usage

1. Prepare input file (data/input/tickers.csv):
```csv
Ticker
AAPL
JPM
O
```

2. Run analysis:
```bash
python main.py --input data/input/tickers.csv --output data/output/results.csv
```

3. Command line arguments:
- `--input`: Input file path
- `--output`: Output file path
- `--type`: Stock type (normal/bank/reit)

## Output Format

The analysis results will include the following columns:
- Stock Code
- Current Price
- Total Score
- Financial Score
- Moat Score
- Risk Deduction
- Target Yield Price
- Relative P/B Price
- PEG Growth Price
- Company Dividend (TTM)
- 5-Year Average Yield
- Company BVPS (TTM)
- 5-Year Average P/B
- Company EPS (TTM)
- Company EPS Growth Rate%

## Scoring Criteria

### Regular Stock Scoring
1. Financial Metrics (11 points max):
   - EPS 10-year stable growth (1 point)
   - Dividend stability and growth (1.5 points)
   - Share count reduction (1 point)
   - Book value growth (1 point)
   - Positive FCF (1 point)
   - Net margin > 10% (1.5 points)
   - ROE performance (1 point)
   - Interest coverage (1.5 points)
   - Debt/Equity ratio (1 point)

2. Competitive Advantages (6 points max):
   - Brand value
   - Patents/Licenses
   - Cost advantages
   - Switching costs
   - Network effects
   - Niche market dominance

3. Risk Deductions (-3 points max):
   - Technology risk (-1)
   - Government policy risk (-1)
   - China ADR risk (-1)

### Bank Stock Scoring
- Asset quality
- Profitability metrics
- Capital adequacy
- Liquidity indicators

### REIT Scoring
- FFO stability
- Distribution policy
- Asset quality
- Debt levels

## Common Issues

1. ModuleNotFoundError:
```bash
pip install -r requirements.txt
```

2. Permission issues:
```bash
chmod +x main.py
```

3. Encoding issues:
```python
df.to_csv('output.csv', encoding='utf-8-sig')
```

## Development

Run tests:
```bash
python -m pytest tests/
```

Check code style:
```bash
flake8 src/
```

Format code:
```bash
black src/
```

## Contributing

1. Fork the project
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

This tool is for educational and research purposes only. Users should verify the data accuracy and assume all risks associated with using this tool for investment decisions.

## Acknowledgments

- Beautiful Soup documentation
- Pandas documentation
- Requests library documentation
- Financial analysis community

## Version History

- 1.0.0
  - Initial Release
  - Basic scraping functionality
  - Three stock type analysis
  - Scoring system implementation