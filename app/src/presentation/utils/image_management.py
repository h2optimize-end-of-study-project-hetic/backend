from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile, HTTPException
from dataclasses import dataclass
import os
import io

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


async def handle_map_image(file: UploadFile, existing_map) -> dict:
    """
    Gère l'image d'une map :
    - si même nom que l'existant : remplacement
    - si nom différent : suppression de l'ancien et sauvegarde du nouveau
    Retourne un dictionnaire avec 'file_name' et 'path' pour la mise à jour de la map.
    """

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")) 
    save_dir = os.path.join(PROJECT_ROOT, "app", "maps")
    os.makedirs(save_dir, exist_ok=True)

    new_file_name = file.filename
    save_path = os.path.join(save_dir, new_file_name)

    # lire le contenu une seule fois
    content = await file.read()

    try:
        image = Image.open(io.BytesIO(content))
        width, length = image.size
    except Exception as e:
        raise ValueError(f"Impossible d'ouvrir l'image : {e}")
    
    # same filename
    if existing_map.file_name == new_file_name:
        # remplacer le fichier existant
        with open(existing_map.path, "wb") as f:
            f.write(content)
        # await save_upload_file(content, existing_map.path)
        return {"path": existing_map.path, "width": width, "length": length}
    else:
        # supprimer l'ancien fichier si il existe
        if os.path.exists(existing_map.path):
            os.remove(existing_map.path)
        # sauvegarder le nouveau
        with open(save_path, "wb") as f:
            f.write(content)
        # await save_upload_file(content, existing_map.path)
        return {"file_name": new_file_name, "path": save_path, "width": width, "length": length}