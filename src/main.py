import os
import random
import logging
from image_utils import load_image, save_image, crop_background, composite_images

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> None:
    """
    Main function to process transparent images and add backgrounds.
    
    This script reads transparent images from `data/transparent`,
    backgrounds from `data/bg-sample`, and saves the composited
    images to `data/output`.
    """
    transparent_dir = 'data/transparent'
    bg_dir = 'data/bg-sample'
    output_dir = 'data/output'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    transparent_images = [f for f in os.listdir(transparent_dir) if f.endswith('.png')]
    background_images = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not background_images:
        logging.warning("No background images found.")
        return

    for transparent_image_name in transparent_images:
        try:
            transparent_image_path = os.path.join(transparent_dir, transparent_image_name)
            transparent_image = load_image(transparent_image_path)

            bg_image_name = random.choice(background_images)
            bg_image_path = os.path.join(bg_dir, bg_image_name)
            background_image = load_image(bg_image_path)

            cropped_bg = crop_background(background_image, transparent_image.width, transparent_image.height)
            final_image = composite_images(cropped_bg, transparent_image)

            output_path = os.path.join(output_dir, transparent_image_name)
            save_image(final_image, output_path)
            logging.info(f"Processed {transparent_image_name}")

        except ValueError as e:
            logging.warning(f"Skipping {transparent_image_name} due to small background: {e}")
        except Exception as e:
            logging.error(f"Error processing {transparent_image_name}: {e}")

if __name__ == "__main__":
    main()
