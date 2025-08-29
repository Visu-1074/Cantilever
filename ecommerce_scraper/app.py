from flask import Flask, render_template, request
import sqlite3, math, os
import pandas as pd

app = Flask(__name__)
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "products.db")

def read_products():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    return df

def filter_df(df, filters):
    # Ensure numeric columns
    if "Price" in df.columns:
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    if "Rating" in df.columns:
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

    if filters.get("q"):
        df = df[df["Title"].str.contains(filters["q"], case=False, na=False)]
    if filters.get("min_price") is not None:
        df = df[df["Price"] >= filters["min_price"]]
    if filters.get("max_price") is not None:
        df = df[df["Price"] <= filters["max_price"]]
    if filters.get("min_rating") is not None:
        df = df[df["Rating"] >= filters["min_rating"]]
    if filters.get("max_rating") is not None:
        df = df[df["Rating"] <= filters["max_rating"]]
    return df

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "").strip() or None
    def pf(s):
        try:
            return float(s)
        except Exception:
            return None
    filters = {
        "q": q,
        "min_price": pf(request.args.get("min_price")),
        "max_price": pf(request.args.get("max_price")),
        "min_rating": pf(request.args.get("min_rating")),
        "max_rating": pf(request.args.get("max_rating")),
    }
    if not os.path.exists(DB_PATH):
        return "<p>Database not found. Run scraper first (python scraper.py).</p>"
    
    df = read_products()
    df = filter_df(df, filters)

    # pagination
    page = int(request.args.get("page", 1))
    per_page = 20
    total = len(df)
    pages = max(1, math.ceil(total / per_page))
    start, end = (page-1)*per_page, (page-1)*per_page + per_page
    view = df.iloc[start:end]

    # Replace NaN with None so template doesn’t show "nan"
    view = view.where(pd.notnull(view), None)

    return render_template("index.html", rows=view.to_dict(orient="records"),
                           total=total, page=page, pages=pages, q=filters["q"],
                           min_price=filters["min_price"], max_price=filters["max_price"],
                           min_rating=filters["min_rating"], max_rating=filters["max_rating"])

if __name__ == "__main__":
    app.run(debug=True)
