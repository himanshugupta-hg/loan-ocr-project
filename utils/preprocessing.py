import cv2
import numpy as np
from pdf2image import convert_from_path
import os

def preprocess_image(image_path, poppler_path=None):
    """Process PDF/image documents with Poppler path support"""
    try:
        if image_path.lower().endswith('.pdf'):
            # Use provided poppler_path or default
            images = convert_from_path(
                image_path,
                poppler_path=poppler_path if poppler_path else None
            )
            
            if not images:
                raise ValueError("PDF conversion failed - empty result")
                
            img = np.array(images[0])
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        else:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Failed to read image: {image_path}")

        # Processing pipeline
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        _, threshold = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY)
        return threshold

    except Exception as e:
        print(f"Preprocessing Error: {str(e)}")
        raise
