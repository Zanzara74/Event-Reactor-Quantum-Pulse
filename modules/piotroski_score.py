import pandas as pd
import os

DATA_DIR = "data/financials"

def load_financial_statement(ticker, report_type):
    """
    Load the CSV file for a given ticker and financial report type.
    report_type: 'income_statement', 'balance_sheet', or 'cash_flow'
    """
    path = os.path.join(DATA_DIR, ticker, f"{report_type}.csv")
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    return pd.read_csv(path)

def calculate_piotroski_score(ticker):
    """
    Calculate Piotroski F-score for the given ticker.
    Returns integer score 0-9 or None if data missing.
    """
    income = load_financial_statement(ticker, "income_statement")
    balance = load_financial_statement(ticker, "balance_sheet")
    cash_flow = load_financial_statement(ticker, "cash_flow")

    if income is None or balance is None or cash_flow is None:
        return None

    # Ensure data is sorted descending by date (most recent first)
    income = income.sort_values(by="date", ascending=False).reset_index(drop=True)
    balance = balance.sort_values(by="date", ascending=False).reset_index(drop=True)
    cash_flow = cash_flow.sort_values(by="date", ascending=False).reset_index(drop=True)

    # Need at least two years to compare
    if len(income) < 2 or len(balance) < 2 or len(cash_flow) < 2:
        return None

    score = 0

    # 1. Positive net income (current year)
    if income.loc[0, "netIncome"] > 0:
        score += 1

    # 2. Positive operating cash flow (current year)
    if cash_flow.loc[0, "operatingCashFlow"] > 0:
        score += 1

    # 3. Higher ROA (net income / total assets) this year vs last year
    roa_curr = income.loc[0, "netIncome"] / balance.loc[0, "totalAssets"]
    roa_prev = income.loc[1, "netIncome"] / balance.loc[1, "totalAssets"]
    if roa_curr > roa_prev:
        score += 1

    # 4. Operating cash flow > net income (quality of earnings)
    if cash_flow.loc[0, "operatingCashFlow"] > income.loc[0, "netIncome"]:
        score += 1

    # 5. Lower leverage ratio (long term debt / total assets) this year vs last year
    lev_curr = balance.loc[0, "longTermDebt"] / balance.loc[0, "totalAssets"]
    lev_prev = balance.loc[1, "longTermDebt"] / balance.loc[1, "totalAssets"]
    if lev_curr < lev_prev:
        score += 1

    # 6. Higher current ratio (current assets / current liabilities) this year vs last year
    curr_ratio_curr = balance.loc[0, "totalCurrentAssets"] / balance.loc[0, "totalCurrentLiabilities"]
    curr_ratio_prev = balance.loc[1, "totalCurrentAssets"] / balance.loc[1, "totalCurrentLiabilities"]
    if curr_ratio_curr > curr_ratio_prev:
        score += 1

    # 7. No new shares issued (shares outstanding current year <= last year)
    shares_curr = balance.loc[0, "commonStockSharesOutstanding"]
    shares_prev = balance.loc[1, "commonStockSharesOutstanding"]
    if shares_curr <= shares_prev:
        score += 1

    # 8. Higher gross margin this year vs last year
    gross_margin_curr = income.loc[0, "grossProfit"] / income.loc[0, "revenue"]
    gross_margin_prev = income.loc[1, "grossProfit"] / income.loc[1, "revenue"]
    if gross_margin_curr > gross_margin_prev:
        score += 1

    # 9. Higher asset turnover (revenue / total assets) this year vs last year
    asset_turnover_curr = income.loc[0, "revenue"] / balance.loc[0, "totalAssets"]
    asset_turnover_prev = income.loc[1, "revenue"] / balance.loc[1, "totalAssets"]
    if asset_turnover_curr > asset_turnover_prev:
        score += 1

    return score

def score(ticker):
    f_score = calculate_piotroski_score(ticker)
    if f_score is None:
        return 0
    # You can adjust threshold if needed, here return 1 if score >= 6
    return 1 if f_score >= 6 else 0


if __name__ == "__main__":
    test_ticker = "AAPL"
    fscore = calculate_piotroski_score(test_ticker)
    print(f"Piotroski score for {test_ticker}: {fscore}")
