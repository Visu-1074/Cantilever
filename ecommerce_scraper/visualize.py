import os, sys
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
xlsx = os.path.join(BASE_DIR, "products.xlsx")
if not os.path.exists(xlsx):
    sys.exit("products.xlsx not found. Run `python scraper.py` first.")

df = pd.read_excel(xlsx)

# Make output folder
out_dir = os.path.join(BASE_DIR, "static")
os.makedirs(out_dir, exist_ok=True)

# --- Handle Price ---
if "Price" in df.columns:
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Price"]).copy()

    # Price Distribution
    if not df["Price"].empty:
        plt.figure(figsize=(8,5))
        df["Price"].plot(kind="hist", bins=20, edgecolor="black")
        plt.title("Price Distribution")
        plt.xlabel("Price (£)")
        plt.ylabel("Count")
        plt.savefig(os.path.join(out_dir, "price_distribution.png"), bbox_inches="tight")
        plt.close()
else:
    print("No 'Price' column found in Excel. Skipping price plots.")

# --- Handle Rating ---
if "Rating" in df.columns:
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

    # Rating vs Price scatter (only if Price also exists)
    if "Price" in df.columns and not df.dropna(subset=["Rating"]).empty:
        plt.figure(figsize=(8,5))
        df.dropna(subset=["Rating"]).plot(kind="scatter", x="Rating", y="Price", alpha=0.7)
        plt.title("Rating vs Price")
        plt.xlabel("Rating")
        plt.ylabel("Price (£)")
        plt.savefig(os.path.join(out_dir, "rating_vs_price.png"), bbox_inches="tight")
        plt.close()
else:
    print("No 'Rating' column found in Excel. Skipping rating plots.")

print("Charts written to", out_dir)

