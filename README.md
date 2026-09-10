# My_Suncsreen — Premium Sunscreen Launch Strategy

A data-driven market analysis and launch strategy for a premium sunscreen brand in India.
Generates synthetic Indian cosmetics market data and provides a Streamlit dashboard
for exploring the data, analyzing competitors, and planning marketing channels.

## Project Structure

```
My_Suncsreen/
├── .github/workflows/     # GitHub Actions CI
├── dashboard/             # Streamlit dashboard app
├── data/
│   ├── external/          # External data sources
│   ├── processed/         # Cleaned/processed datasets
│   └── raw/               # Generated raw datasets
├── notebooks/             # Jupyter notebooks for analysis
├── reports/               # Generated reports and slides
├── src/
│   └── generate_data.py   # Synthetic data generation
└── tests/                 # Unit tests
```

## Setup

```bash
git clone https://github.com/Aditya01Jhajhra/My_Suncsreen.git
cd My_Suncsreen
pip install -r requirements.txt
```

## Usage

### Generate datasets
```bash
python src/generate_data.py
```

### Run the dashboard
```bash
streamlit run dashboard/app.py
```

### Run tests
```bash
pytest tests/
```

## Datasets Generated

| File | Description |
|------|-------------|
| `Indian_Cosmetics_Products.csv` | 850 products across 10 brands |
| `Customers.csv` | 3,500 customers with demographics |
| `Orders.csv` | 12,000 orders with pricing/discounts |
| `Competitor_Products.csv` | 10 competitor sunscreen products |
| `City_Metrics.csv` | 10 Indian cities with market metrics |
| `Marketing_Channels.csv` | 6 marketing channel benchmarks |
| `Customer_Insights.csv` | Customer-level insights for modeling |

## License
MIT