# StockMarket

## Background
This is a side project created for solving the basic problem of finding data of multiple stocks.

Get PE ratio and color code each them Yellow if PE is between 24-30, orange for 30-50 and red if its greater than 50.

At how much discount are we getting the stocks for?

## Contents
This repo code to analyse stock market data from screenr.in website and loads certain data like
- PE (Price/Earning ratio)
- Stock price
- ROCE (Return on Capital Employed) - long-term profitability ratio that shows how much profit a company generates for each unit of currency it employs.
- 52 weeks High, low
- Percentage from High and low.

Can enhance more as and when required.

This repo also contains [stock_symbols.py](stock_symbols.py) file that contains the ticker of each stock. To update this, open the stock in screenr.in and paste the ticker in this file.

## Dependencies
```
pip3 install requests flask flask_bootstrap pandas openpyxl
```
## Status

[![Deploy to PythonAnywhere](https://github.com/shreekant/StockMarket/actions/workflows/deploy.yml/badge.svg?branch=master)](https://github.com/shreekant/StockMarket/actions/workflows/deploy.yml)
