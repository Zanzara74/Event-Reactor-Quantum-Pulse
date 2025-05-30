import requests

def fetch_financials(ticker):
    """
    Fetch key financial data from FinancialModelingPrep or other API.
    Return a dict with needed financial ratios and values.
    This is a placeholder; you need to replace with your API call and parsing.
    """
    # Example placeholder response
    data = {
        'net_income': 1000000,
        'operating_cash_flow': 900000,
        'return_on_assets': 0.08,
        'leverage': 0.4,
        'liquidity': 1.5,
        'shares_outstanding': 1000000,
        'gross_margin': 0.5,
        'asset_turnover': 0.9,
    }
    return data

def score(ticker):
    """
    Calculate Piotroski F-Score for a ticker.
    Return score 0-9.
    """
    data = fetch_financials(ticker)
    f_score = 0

    # 1. Positive net income
    if data['net_income'] > 0:
        f_score += 1
    # 2. Positive operating cash flow
    if data['operating_cash_flow'] > 0:
        f_score += 1
    # 3. Higher ROA than previous year (placeholder: assume True)
    f_score += 1
    # 4. Operating cash flow > net income
    if data['operating_cash_flow'] > data['net_income']:
        f_score += 1
    # 5. Lower leverage (placeholder)
    f_score += 1
    # 6. Higher current ratio (liquidity) than previous year (placeholder)
    f_score += 1
    # 7. No new shares issued (placeholder)
    f_score += 1
    # 8. Higher gross margin than previous year (placeholder)
    f_score += 1
    # 9. Higher asset turnover than previous year (placeholder)
    f_score += 1

    return f_score
