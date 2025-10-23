from PIL import Image
from pathlib import Path
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset

class LogoDataset(Dataset):
    def __init__(self, images, masks, transform=None):
        self.images = images
        self.masks = masks
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx].convert("RGB")
        mask = self.masks[idx].convert("L")

        if self.transform:
            image = self.transform(image)
            mask = self.transform(mask)

        return image, mask

def load_data(input_dir, mask_dir):
    """
    Loads images and masks from the specified directories.

    Args:
        input_dir (str): Path to the directory of training images.
        mask_dir (str): Path to the directory of mask images.

    Returns:
        tuple: A tuple containing training, validation, and test data splits.
    """
    input_path = Path(input_dir)
    mask_path = Path(mask_dir)

    image_files = sorted([p for p in input_path.glob("*.png")])
    mask_files = sorted([p for p in mask_path.glob("*.png")])

    if len(image_files) != len(mask_files):
        print(f"Warning: Mismatched number of images and masks. Found {len(image_files)} images and {len(mask_files)} masks.")
        # Use the intersection of filenames
        image_names = {p.name for p in image_files}
        mask_names = {p.name for p in mask_files}
        common_names = sorted(list(image_names.intersection(mask_names)))
        
        image_files = [input_path / name for name in common_names]
        mask_files = [mask_path / name for name in common_names]

    images = [Image.open(p) for p in image_files]
    masks = [Image.open(p) for p in mask_files]

    X_train, X_val, y_train, y_val = train_test_split(images, masks, test_size=0.15, random_state=42)

    return X_train, X_val, y_train, y_val
