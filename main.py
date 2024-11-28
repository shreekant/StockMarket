import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def get_details_of_stock(stock_symbol):
    url = f"https://www.screener.in/company/{stock_symbol}/consolidated"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        pe_ratio_element = soup.find('span', string=lambda x: x and 'P/E' in x)
        high_low_element = soup.find('span', string=lambda x: x and 'High / Low' in x)
        roce_element = soup.find('span', string=lambda x: x and 'ROCE' in x)
        current_price_element = soup.find('span', string=lambda x: x and 'Current Price' in x)

        if pe_ratio_element:
            pe_ratio = pe_ratio_element.find_next_sibling('span').text.strip() if pe_ratio_element else "P/E ratio not found"
            high_low_value = high_low_element.find_next_sibling('span').text.strip() if high_low_element else "High/Low not found"
            roce_value = roce_element.find_next_sibling('span').text.strip() if roce_element else "ROCE not found"
            roce_value = re.sub(r'[^\d.]', '', roce_value)  # Remove special characters except decimal point
            current_price = current_price_element.find_next_sibling('span').text.strip() if current_price_element else "Current Price not found"
            current_price = re.sub(r'[^\d.]', '', current_price)  # Remove special characters except decimal point

            # Split High/Low value
            high, low = high_low_value.split('/')
            high = re.sub(r'[^\d.]', '', high.strip())
            low = re.sub(r'[^\d.]', '', low.strip())

            # Calculate percentage change from high and low to current price
            high_value = float(high)
            low_value = float(low)
            current_price_value = float(current_price)
            percentage_change_from_high = ((current_price_value - high_value) / high_value) * 100
            percentage_change_from_low = ((current_price_value - low_value) / low_value) * 100

            # Convert PE ratio to float if possible
            try:
                pe_ratio_value = float(pe_ratio)
            except ValueError:
                pe_ratio_value = None

            return {
                "Symbol": stock_symbol,
                "PE Ratio": pe_ratio_value,
                "Current Price": current_price_value,
                "High": high_value,
                "Low": low_value,
                "ROCE": float(roce_value),
                "Percentage change from high": percentage_change_from_high,
                "Percentage change from low": percentage_change_from_low
            }
        else:
            return None
    else:
        return None

stock_symbols = [
    'HINDUNILVR','TCS', '5PAISA', 'ADANIPORTS', 'ARMANFIN', 'AXISBANK', 'BAJAJ-AUTO',
    'BHEL', 'CDSL', 'SWIGGY'
    ]
stock_details_list = []

for symbol in stock_symbols:
    stock_details = get_details_of_stock(symbol)
    if stock_details:
        stock_details_list.append(stock_details)

# Create a DataFrame and save to Excel
df = pd.DataFrame(stock_details_list)
excel_filename = 'stock_details.xlsx'
df.to_excel(excel_filename, index=False)

# Load the workbook and select the active worksheet
wb = load_workbook(excel_filename)
ws = wb.active

# Define the red fill for conditional formatting
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

# Apply conditional formatting to rows where PE Ratio is more than 50
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
    pe_ratio_cell = row[1]  # Assuming PE Ratio is in the second column
    if pe_ratio_cell.value is not None and pe_ratio_cell.value > 50:
        for cell in row:
            cell.fill = red_fill

# Auto-adjust column widths based on the title
for column in ws.columns:
    max_length = 0
    column = list(column)
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column[0].column_letter].width = adjusted_width

# Save the workbook with the applied formatting
wb.save(excel_filename)

print(f'Stock details saved to {excel_filename}')
