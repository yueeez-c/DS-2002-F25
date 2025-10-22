def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        print(f"Portfolio file {portfolio_file} does not exist.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(portfolio_file)
    if df.empty:
        print("Portfolio is empty.", file=sys.stderr)
        return
    total_value = df['card_market_value'].sum()
    ix = df.idxmax('card_market_value')
    most_valuable_card = df.loc[ix]
    print(f"Total Portfolio Value: ${total_value:.2f}")
    print("Most Valuable Card:")
    print(f"  Name: {most_valuable_card['card_name']}")
    print(f"  ID: {most_valuable_card['card_id']}")
    print(f"  Market Value: ${most_valuable_card['card_market_value']:.

def main():
    generate_summary('card_portfolio.csv')
def test():
    generate_summary('test_card_portfolio.csv')
if __name__ == "__main__":
    # Log to stderr that the script is starting in Test Mode
    print("Starting script in Test Mode", file=sys.stderr)
    test()
