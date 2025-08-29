from flask import Flask, render_template, request, flash
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = "dev"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract OCR\tesseract.exe"

# Allowed image extensions
ALLOWED = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

@app.route("/", methods=["GET", "POST"])
def home():
    texts = {}  # Dictionary to store filename -> extracted text
    if request.method == "POST":
        # Option 1: Upload images manually
        f = request.files.get("file")
        if f and f.filename != "":
            ext = os.path.splitext(f.filename)[1].lower()
            if ext in ALLOWED:
                path = os.path.join(UPLOAD_FOLDER, f.filename)
                f.save(path)
                img = Image.open(path).convert("L")
                text = pytesseract.image_to_string(img).strip()
                texts[f.filename] = text
                os.remove(path)
            else:
                flash("Unsupported file type.")
        # Option 2: Process all images in dataset folder
        elif request.form.get("process_dataset"):
            dataset_folder = os.path.join(os.path.dirname(__file__), "dataset")
            for file in os.listdir(dataset_folder):
                if file.lower().endswith(tuple(ALLOWED)):
                    path = os.path.join(dataset_folder, file)
                    img = Image.open(path).convert("L")
                    text = pytesseract.image_to_string(img).strip()
                    texts[file] = text
        else:
            flash("Please choose an image file or process dataset.")
    return render_template("index.html", texts=texts)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
