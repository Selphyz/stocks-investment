#%%
import requests
import pandas as pd
import os
import re
from sec_edgar_downloader import Downloader

#%%
def download_10k_filing(ticker, year=None, output_dir='sec_filings'):
    """
    Download the most recent 10-K filing or a specific year's filing for a given ticker

    Parameters:
    - ticker (str): Stock ticker symbol
    - year (int, optional): Specific year of filing
    - output_dir (str): Directory to save downloaded filings

    Returns:
    str: Path to downloaded filing
    """
    # Create download directory
    os.makedirs(output_dir, exist_ok=True)

    # Initialize downloader
    dl = Downloader(output_dir)

    try:
        # If no year specified, download most recent
        if year is None:
            filing = dl.get_10k_filings(ticker, limit=1)
        else:
            filing = dl.get_10k_filings(ticker, year=year, limit=1)

        # Return path to first downloaded filing
        return filing[0] if filing else None
    except Exception as e:
        print(f"Error downloading 10-K for {ticker}: {e}")
        return None

#%%
def extract_regex_ratios(filing_path):
    """
    Extract financial ratios from 10-K filing using regex patterns

    Parameters:
    - filing_path (str): Path to downloaded 10-K filing

    Returns:
    dict: Extracted financial ratios
    """
    ratios = {
        'PER': None,  # Price to Earnings Ratio
        'ROC': None,  # Return on Capital
        'ROI': None,  # Return on Investment
        'ROIC': None,  # Return on Invested Capital
        'ROE': None   # Return on Equity
    }

    try:
        # Read the filing
        with open(filing_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

            # Regular expressions to extract ratios
            ratio_patterns = {
                'PER': r'Price\s*to\s*Earnings\s*Ratio[:\s]*(\d+\.?\d*)',
                'ROC': r'Return\s*on\s*Capital[:\s]*(\d+\.?\d*)%',
                'ROI': r'Return\s*on\s*Investment[:\s]*(\d+\.?\d*)%',
                'ROIC': r'Return\s*on\s*Invested\s*Capital[:\s]*(\d+\.?\d*)%',
                'ROE': r'Return\s*on\s*Equity[:\s]*(\d+\.?\d*)%'
            }

            # Extract ratios using regex
            for ratio_key, pattern in ratio_patterns.items():
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    ratios[ratio_key] = float(match.group(1))

        return ratios
    except Exception as e:
        print(f"Error extracting ratios: {e}")
        return ratios

#%%
def calculate_ratios_from_statements(filing_path):
    """
    Calculate financial ratios from extracted financial statement data

    Parameters:
    - filing_path (str): Path to downloaded 10-K filing

    Returns:
    dict: Calculated financial ratios
    """
    try:
        # These calculations are simplified and may require more complex parsing
        ratios = {
            'ROE': None,
            'ROIC': None,
            'ROI': None,
            'ROC': None
        }

        # Read filing content
        with open(filing_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

            # Example extractions (very simplified)
            net_income_match = re.search(r'Net\s*Income[:\s]*\$?(\d+\.?\d*)', content)
            total_equity_match = re.search(r'Total\s*Equity[:\s]*\$?(\d+\.?\d*)', content)

            if net_income_match and total_equity_match:
                net_income = float(net_income_match.group(1))
                total_equity = float(total_equity_match.group(1))

                # Basic ROE calculation
                ratios['ROE'] = (net_income / total_equity) * 100 if total_equity != 0 else None

        return ratios
    except Exception as e:
        print(f"Error calculating ratios: {e}")
        return None

#%%
def get_financial_ratios(ticker, year=None):
    """
    Retrieve financial ratios for a given ticker

    Parameters:
    - ticker (str): Stock ticker symbol
    - year (int, optional): Specific year of filing

    Returns:
    dict: Financial ratios
    """
    # Download 10-K filing
    filing_path = download_10k_filing(ticker, year)

    if not filing_path:
        print(f"Could not download filing for {ticker}")
        return None

    # Extract and calculate ratios
    extracted_ratios = extract_regex_ratios(filing_path)
    calculated_ratios = calculate_ratios_from_statements(filing_path)

    # Merge extracted and calculated ratios
    if calculated_ratios:
        extracted_ratios.update({k: v for k, v in calculated_ratios.items() if v is not None})

    return extracted_ratios

#%%
tickers = ['AAPL', 'GOOGL', 'MSFT']
years = [2022, 2021, 2020]

for ticker in tickers:
    for year in years:
        print(f"\nRetrieving ratios for {ticker} in {year}:")
        ratios = get_financial_ratios(ticker, year)

        if ratios:
            for ratio, value in ratios.items():
                print(f"{ratio}: {value}")