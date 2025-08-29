# Cantilever Internship Project

This repository contains two beginner-friendly projects for your Cantilever internship:

1. **E-commerce Web Scraper + Analysis + Flask UI**
   - Scrapes book data (Title, Price, Rating, Description, Product URL, Image URL) from Books to Scrape.
   - Saves data to products.xlsx and products.db (SQLite).
   - Generates charts (price distribution, rating vs price) in `ecommerce_scraper/static/`.
   - Flask UI allows searching and filtering by title, price, and rating.

2. **OCR Web App**
   - Upload an image and extract text using Tesseract OCR (pytesseract).
   - Small Flask app with file-type checks and friendly flash messages.

## Quick Start (local machine)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the scraper (creates products.xlsx & products.db):
   ```bash
   cd ecommerce_scraper
   python scraper.py --pages 3
   ```

3. Make charts:
   ```bash
   python visualize.py
   ```

4. Run the web UI (scraper app):
   ```bash
   python app.py
   ```
   Open http://127.0.0.1:5000

5. Run the OCR app (in a new terminal):
   ```bash
   cd ../ocr_app
   # On Windows, install Tesseract OCR engine separately and set path in app.py if needed.
   python app.py
   ```
   Open http://127.0.0.1:5001 (app uses port 5001 by default to avoid conflict)

## Notes
- **Tesseract engine** must be installed separately on your machine for pytesseract to work.
  - Windows example: install Tesseract and set `pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"`
- This project is designed for learning and may need selector updates if adapted to other e-commerce sites.




Author: Vishal Yadav
Role: Cantilever Internship Participant
