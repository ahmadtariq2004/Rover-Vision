from pathlib import Path
import shutil

import cv2
import pytesseract
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from ultralytics import YOLO


ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def configure_tesseract():
    """Use PATH or the default Windows installation location when available."""
    executable = shutil.which('tesseract')
    default_windows_path = Path(r'C:\Program Files\Tesseract-OCR\tesseract.exe')

    if executable:
        pytesseract.pytesseract.tesseract_cmd = executable
    elif default_windows_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(default_windows_path)


def home(request):
    """Upload an image and run the selected OCR or YOLO analysis."""
    context = {}

    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        mode = request.POST.get('mode', 'OCR')

        if not uploaded_image:
            context['error'] = 'Please choose a JPG or PNG image.'
            return render(request, 'index.html', context)

        if Path(uploaded_image.name).suffix.lower() not in ALLOWED_EXTENSIONS:
            context['error'] = 'Only JPG, JPEG, and PNG images are supported.'
            return render(request, 'index.html', context)

        if mode not in {'OCR', 'YOLO'}:
            context['error'] = 'Please select a valid analysis mode.'
            return render(request, 'index.html', context)

        storage = FileSystemStorage()
        filename = storage.save(uploaded_image.name, uploaded_image)
        image_path = storage.path(filename)
        context['image_url'] = storage.url(filename)

        if mode == 'OCR':
            image = cv2.imread(image_path)
            if image is None:
                context['error'] = 'The uploaded image could not be read.'
            else:
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                try:
                    configure_tesseract()
                    extracted_text = pytesseract.image_to_string(grayscale_image).strip()
                    context['result'] = extracted_text or 'No text was detected.'
                except pytesseract.TesseractNotFoundError:
                    context['error'] = (
                        'OCR engine is not installed. Install Tesseract OCR on Windows, '
                        'then restart the Django server.'
                    )
                    context['result'] = 'OCR is currently unavailable.'
        else:
            model = YOLO('yolov8n.pt')
            results = model(image_path)
            detected_count = sum(len(result.boxes) for result in results)
            context['result'] = f'Detected objects: {detected_count}'

    return render(request, 'index.html', context)
