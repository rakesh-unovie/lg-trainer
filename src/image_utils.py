from PIL import Image
import random
from typing import Tuple

def load_image(image_path: str) -> Image.Image:
    """
    Loads an image from a file path.

    Args:
        image_path: The path to the image file.

    Returns:
        A Pillow Image object.
    """
    return Image.open(image_path)

def save_image(image: Image.Image, save_path: str) -> None:
    """
    Saves an image to a file path.

    Args:
        image: The Pillow Image object to save.
        save_path: The path to save the image to.
    """
    image.save(save_path)

def crop_background(background: Image.Image, width: int, height: int) -> Image.Image:
    """
    Crops a random area from the background image.

    Args:
        background: The background image.
        width: The width of the desired crop.
        height: The height of the desired crop.

    Returns:
        The cropped background image.
        
    Raises:
        ValueError: If the background image is smaller than the desired crop dimensions.
    """
    if background.width < width or background.height < height:
        raise ValueError("Background image is smaller than the foreground image.")
    
    left = random.randint(0, background.width - width)
    top = random.randint(0, background.height - height)
    right = left + width
    bottom = top + height
    
    return background.crop((left, top, right, bottom))

def composite_images(background: Image.Image, foreground: Image.Image) -> Image.Image:
    """
    Composites a foreground image onto a background image.
    The foreground image should have an alpha channel.

    Args:
        background: The background image.
        foreground: The foreground image.

    Returns:
        The composited image.
    """
    background.paste(foreground, (0, 0), foreground)
    return background

def preprocess_image(image_path: str) -> Image.Image:
    """
    Loads, preprocesses, and returns an image.

    - Handles alpha channels by flattening onto a white background.
    - Converts to RGB.
    - Resizes to 320x320.
    - Handles corrupted images.

    Args:
        image_path: The path to the image file.

    Returns:
        A processed Pillow Image object, or None if the image is corrupt.
    """
    try:
        image = Image.open(image_path)

        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background

        image = image.convert('RGB')
        image = image.resize((320, 320), Image.Resampling.LANCZOS)
        
        return image
    except Image.UnidentifiedImageError:
        print(f"Warning: Corrupted image detected and skipped: {image_path}")
        return None
