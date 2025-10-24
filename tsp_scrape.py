#!/usr/bin/python3
# Script to scrape TSP fund prices from tsp.gov and reformat for Ghostfolio import

import requests
import csv
import sys
import os

# Map TSP CSV headers to Ghostfolio symbols
fund_map = {
    "L Income": "TSP_LINC",
    "L 2030": "TSP_L2030",
    "L 2035": "TSP_L2035",
    "L 2040": "TSP_L2040",
    "L 2045": "TSP_L2045",
    "L 2050": "TSP_L2050",
    "L 2055": "TSP_L2055",
    "L 2060": "TSP_L2060",
    "L 2065": "TSP_L2065",
    "L 2070": "TSP_L2070",
    "L 2075": "TSP_L2075",
    "G Fund": "TSP_G",
    "F Fund": "TSP_F",
    "C Fund": "TSP_C",
    "S Fund": "TSP_S",
    "I Fund": "TSP_I",
}

outputDir = "tsp_prices"
os.makedirs(outputDir, exist_ok=True)

# Download the official CSV from TSP
url = "https://www.tsp.gov/data/fund-price-history.csv"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}
resp = requests.get(url, headers=headers)
if resp.status_code != 200:
    print("❌ Failed to fetch TSP data:", resp.status_code)
    sys.exit(1)

reader = csv.DictReader(resp.text.splitlines())

# Prepare file handles for each fund
writers = {}
files = {}
for col, symbol in fund_map.items():
    fpath = os.path.join(outputDir, f"{symbol}.csv")
    f = open(fpath, "w", newline="")
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["date", "marketPrice"])
    writers[col] = writer
    files[col] = f

# Process rows
for row in reader:
    if not row["Date"]:
        continue
    
    dt = row["Date"].strip()

    for col, symbol in fund_map.items():
        price_str = row.get(col, "").strip()
        if not price_str:
            continue
        try:
            price = float(price_str)
        except ValueError:
            continue
        writers[col].writerow([dt, price])

# Close all files
for f in files.values():
    f.close()

print(f"✅ Wrote one CSV per fund into {outputDir}/")
