import unittest
from PIL import Image
import os
from src.image_utils import crop_background, composite_images, preprocess_image

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


class TestPreprocessImage(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_images"
        os.makedirs(self.test_dir, exist_ok=True)

        # Create a dummy RGBA image
        self.rgba_path = os.path.join(self.test_dir, "rgba.png")
        Image.new('RGBA', (100, 100), (255, 0, 0, 128)).save(self.rgba_path)

        # Create a dummy RGB image
        self.rgb_path = os.path.join(self.test_dir, "rgb.jpg")
        Image.new('RGB', (150, 150), (0, 255, 0)).save(self.rgb_path)

        # Create a dummy corrupted image
        self.corrupted_path = os.path.join(self.test_dir, "corrupted.jpg")
        with open(self.corrupted_path, 'w') as f:
            f.write("this is not an image")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_preprocess_rgba(self):
        image = preprocess_image(self.rgba_path)
        self.assertEqual(image.mode, 'RGB')
        self.assertEqual(image.size, (320, 320))
        # Check that the background is white where the image was transparent
        self.assertEqual(image.getpixel((0, 0)), (255, 127, 127))

    def test_preprocess_rgb(self):
        image = preprocess_image(self.rgb_path)
        self.assertEqual(image.mode, 'RGB')
        self.assertEqual(image.size, (320, 320))

    def test_preprocess_corrupted(self):
        image = preprocess_image(self.corrupted_path)
        self.assertIsNone(image)


if __name__ == '__main__':
    unittest.main()
