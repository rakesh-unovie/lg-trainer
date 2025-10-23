import unittest
from PIL import Image
import os
from src.image_utils import crop_background, composite_images

class TestImageUtils(unittest.TestCase):
    def setUp(self):
        # Create a dummy background image for testing
        self.background = Image.new('RGB', (200, 200), color = 'red')
        self.foreground = Image.new('RGBA', (100, 100), color = (0, 255, 0, 255))

    def test_crop_background(self):
        width, height = 100, 100
        cropped_image = crop_background(self.background, width, height)
        self.assertEqual(cropped_image.size, (width, height))

    def test_crop_background_too_small(self):
        with self.assertRaises(ValueError):
            crop_background(self.background, 300, 300)

    def test_composite_images(self):
        composited_image = composite_images(self.background.copy(), self.foreground)
        # Check a pixel to see if the foreground was pasted
        self.assertEqual(composited_image.getpixel((50, 50)), (0, 255, 0))




if __name__ == '__main__':
    unittest.main()
