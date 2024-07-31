import yfinance as yf
import pandas as pd

# Function to fetch stock details
def fetch_stock_details(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    # Extract relevant information
    stock_details = {
        'Ticker': ticker,
        'Company Name': stock_info.get('longName', 'N/A'),
        'Price' : stock_info.get('currentPrice', 'N/A'),
        'PE Ratio': stock_info.get('trailingPE', 'N/A'),
        'Market Cap': stock_info.get('marketCap', 'N/A'),
        'Previous Close': stock_info.get('previousClose', 'N/A'),
        '52 Week High': stock_info.get('fiftyTwoWeekHigh', 'N/A'),
        '52 Week Low': stock_info.get('fiftyTwoWeekLow', 'N/A'),
    }
    print(stock_details)
    return stock_details

# List of stock tickers
tickers = [ 'AAVAS.NS', 'BHEL.NS']

# Fetch stock details for each ticker
stock_data = []
for ticker in tickers:
    details = fetch_stock_details(ticker)
    stock_data.append(details)

# Create a DataFrame
df = pd.DataFrame(stock_data)

# Save the DataFrame to an Excel file
excel_filename = 'stock_details.xlsx'
df.to_excel(excel_filename, index=False)

print(f'Stock details saved to {excel_filename}')
