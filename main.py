import requests
from bs4 import BeautifulSoup
import re

def get_details_of_stock(stock_symbol):
    url = f"https://www.screener.in/company/{stock_symbol}/consolidated"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        pe_ratio_element = soup.find('span', string=lambda x: x and 'P/E' in x)
        high_low_element = soup.find('span', string=lambda x: x and 'High / Low' in x)
        roce_element = soup.find('span', string=lambda x: x and 'ROCE' in x)
        current_price = soup.find('span', string=lambda x: x and 'Current Price' in x)

        if pe_ratio_element:
            pe_ratio = pe_ratio_element.find_next_sibling('span').text.strip() if pe_ratio_element else "P/E ratio not found"
            high_low_value = high_low_element.find_next_sibling('span').text.strip() if high_low_element else "High/Low not found"
            roce_value = roce_element.find_next_sibling('span').text.strip() if roce_element else "ROCE not found"
            roce_value = re.sub(r'[^\d.]', '', roce_value)  # Remove special characters except decimal point
            current_price = current_price.find_next_sibling('span').text.strip() if current_price else "Current Price not found"
            current_price = re.sub(r'[^\d.]', '', current_price)  # Remove special characters

            # Split High/Low value
            high, low = high_low_value.split('/')
            high = re.sub(r'[^\d.]', '', high.strip())
            low = re.sub(r'[^\d.]', '', low.strip())

            high_value = float(high)
            low_value = float(low)
            current_price_value = float(current_price)
            percentage_change = ((current_price_value - high_value) / high_value) * 100
            percentage_change_from_low = ((current_price_value - low_value) / low_value) * 100


            return {
                "PE_Ratio": pe_ratio,
                "Current_price": current_price,
                "High": high,
                "Low": low,
                "ROCE": roce_value,
                "Percentage_change_from_high": f"{percentage_change:.1f}%",
                "Percentage_change_from_low": f"{percentage_change_from_low:.1f}%"
            }
        else:
            return "PE Ratio not found"
    else:
        return f"Failed to retrieve data for {stock_symbol}"

# Example usage:
stock_symbols = ['HINDUNILVR','TCS', '5PAISA', 'ADANIPORTS']  # Replace with actual stock symbols
for symbol in stock_symbols:
    stock_details = get_details_of_stock(symbol)
    print(f"{symbol}: {stock_details}")