from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile, HTTPException
from dataclasses import dataclass

@dataclass
class ImageInfo:
    format: str
    width: int
    length: int

def process_image(file: UploadFile) -> dict:
    """
    Check file format and read metadata
    return class with format width and length
    """
    try:
        file.file.seek(0)
        with Image.open(file.file) as img:
            img.verify() 
            format = img.format
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="The file is not a valid image")

    if format not in ["PNG", "JPEG", "WEBP"]: 
        raise HTTPException(status_code=400, detail="Unsupported image format")

    # Read metadata
    file.file.seek(0)
    with Image.open(file.file) as img:
        width, length = img.size

    return ImageInfo(format=format, width=width, length=length)
