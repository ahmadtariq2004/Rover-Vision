# Rover Vision

Rover Vision is a Django web app for local image analysis. Upload a JPG, JPEG, or PNG image and choose one of two analysis modes:

- **OCR**: extracts readable text from the image using OpenCV and Tesseract OCR.
- **YOLO**: detects objects using the included `yolov8n.pt` Ultralytics model.

## Requirements

- Python 3.10 or newer
- Windows (the OCR helper includes the default Windows Tesseract path)
- Tesseract OCR for OCR mode
- Internet access on the first Ultralytics/PyTorch setup if the required packages are not already installed

## Setup on Windows

Open PowerShell in this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install django opencv-python pytesseract ultralytics
```

Install Tesseract OCR separately for OCR mode. The app checks the system `PATH` first and then checks:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is installed elsewhere, add its folder to the Windows `PATH` and restart the terminal/server.

## Run the project

Apply database migrations, check the project, and start the development server:

```powershell
python manage.py migrate
python manage.py check
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in a browser.

## How to use

1. Choose a JPG, JPEG, or PNG image.
2. Select `OCR / Extract text` or `YOLO / Detect objects`.
3. Press the start button and wait for the analysis result.
4. Uploaded images are stored in the local `media/` directory during development.

## Project layout

```text
manage.py                 Django command-line entry point
ai_app/                   Upload and analysis view plus template
core/                     Django settings, URLs, ASGI and WSGI
yolov8n.pt               Local YOLOv8 nano model
db.sqlite3                Development SQLite database
media/                    Uploaded images
```

## Notes

- This configuration is for local development only. Do not use `DEBUG = True` or the development server in production.
- OCR depends on the external Tesseract executable; YOLO depends on the included model and Ultralytics/PyTorch installation.
- The project accepts only `.jpg`, `.jpeg`, and `.png` uploads.
