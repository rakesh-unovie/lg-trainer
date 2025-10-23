
import os
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_masks() -> None:
    """
    Generates black and white masks from the alpha channel of transparent images.

    This script reads transparent PNG images from `data/transparent`,
    extracts their alpha channel, converts it to a grayscale image,
    and saves the resulting mask to `data/masks`.
    """
    transparent_dir = 'data/transparent'
    masks_dir = 'data/masks'

    if not os.path.exists(masks_dir):
        os.makedirs(masks_dir)
        logging.info(f"Created directory: {masks_dir}")

    transparent_images = [f for f in os.listdir(transparent_dir) if f.endswith('.png')]

    if not transparent_images:
        logging.warning(f"No transparent images found in {transparent_dir}.")
        return

    logging.info(f"Found {len(transparent_images)} transparent images to process.")

    for image_name in transparent_images:
        try:
            image_path = os.path.join(transparent_dir, image_name)
            with Image.open(image_path) as img:
                if img.mode == 'RGBA':
                    # Get the alpha channel
                    alpha = img.getchannel('A')
                    
                    # Convert alpha channel to a binary mask
                    mask = alpha.point(lambda p: 255 if p > 0 else 0, 'L')
                    
                    # Save the mask
                    mask_path = os.path.join(masks_dir, image_name)
                    mask.save(mask_path)
                    logging.info(f"Successfully created mask for {image_name}")
                else:
                    logging.warning(f"Image {image_name} is not in RGBA mode and will be skipped.")

        except Exception as e:
            logging.error(f"Error processing {image_name}: {e}")

if __name__ == "__main__":
    create_masks()
