from PIL import Image
import pytesseract
import os

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract OCR\tesseract.exe"

dataset_folder = "dataset"  # Your dataset folder path

for file in os.listdir(dataset_folder):
    if file.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")):
        path = os.path.join(dataset_folder, file)
        img = Image.open(path).convert("L")
        text = pytesseract.image_to_string(img)
        print(f"File: {file}")
        print("Extracted Text:")
        print(text)
        print("-"*50)
