import os

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def validate_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")
    return True
