from modules import piotroski_score

def test_piotroski(ticker):
    score = piotroski_score.calculate_piotroski_score(ticker)
    if score is None:
        print(f"No sufficient data to calculate Piotroski score for {ticker}")
    else:
        print(f"Piotroski score for {ticker}: {score}")

if __name__ == "__main__":
    test_piotroski("AAPL")  # replace with any ticker you have data for
