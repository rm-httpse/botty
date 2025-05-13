import io
import base64
from PIL import Image

def image_to_base64(img: Image.Image, format: str = "JPEG") -> str:
    buffered = io.BytesIO()
    if format.upper() == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")
    img.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")