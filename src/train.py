import argparse
import torch
import os
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from rembg import new_session
from torch.hub import load_state_dict_from_url
from tqdm import tqdm
import time
from pathlib import Path
from PIL import Image
from sklearn.model_selection import train_test_split

from data_loader import load_data, LogoDataset
from u2net_model import U2NET


def main():
    parser = argparse.ArgumentParser(description="Train a U2-Net model for logo detection.")
    parser.add_argument("--input_dir", type=str, required=True, help="Path to the directory of training images.")
    parser.add_argument("--mask_dir", type=str, required=True, help="Path to the directory of mask images.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the trained model file.")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs.")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size for training.")
    parser.add_argument("--learning_rate", type=float, default=0.001, help="Learning rate for the optimizer.")
    parser.add_argument("--model_path", type=str, default="~/.u2net/u2net.pth", help="Path to the pre-trained model file.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    mask_dir = Path(args.mask_dir)

    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
    ])

    X_train, X_val, y_train, y_val = load_data(input_dir, mask_dir)
    
    train_dataset = LogoDataset(X_train, y_train, transform=transform)
    val_dataset = LogoDataset(X_val, y_val, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    # This will trigger the download of the model if it's not already cached.
    new_session("u2net")
    model_path = os.path.expanduser(args.model_path)
    
    model = U2NET()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'), weights_only=False))
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    criterion = torch.nn.BCEWithLogitsLoss()

    for epoch in range(args.epochs):
        model.train()
        for images, masks in tqdm(train_loader, desc=f"Epoch {epoch+1}/{args.epochs}"):
            images, masks = images.to(device), masks.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs[0], masks)
            loss.backward()
            optimizer.step()

        model.eval()
        total_iou = 0
        with torch.no_grad():
            for images, masks in val_loader:
                images, masks = images.to(device), masks.to(device)
                outputs = model(images)
                preds = torch.sigmoid(outputs[0]) > 0.5
                
                intersection = torch.logical_and(preds, masks).sum()
                union = torch.logical_or(preds, masks).sum()
                iou = intersection / union
                total_iou += iou.item()
        
        avg_iou = total_iou / len(val_loader)
        print(f"Epoch {epoch+1}/{args.epochs}, Validation IoU: {avg_iou:.4f}")

    output_path = Path(args.output_path)
    if output_path.exists():
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = output_path.with_name(f"{output_path.stem}_{timestamp}{output_path.suffix}")
    
    torch.save(model.state_dict(), output_path)
    print(f"Model saved to {output_path}")

if __name__ == "__main__":
    main()