"""
Example: Simple Image Classification with PyTorch

This example demonstrates how to:
1. Load a pre-trained model
2. Process an image
3. Make predictions using GPU acceleration
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch  # noqa: E402
import torchvision.models as models  # noqa: E402
import torchvision.transforms as transforms  # noqa: E402
from PIL import Image  # noqa: E402
from src.utils import get_device, set_seed  # noqa: E402


def load_model(device):
    """Load a pre-trained ResNet model."""
    print("Loading pre-trained ResNet18 model...")
    model = models.resnet18(pretrained=True)
    model = model.to(device)
    model.eval()
    print("Model loaded successfully!")
    return model


def preprocess_image(image_path):
    """Preprocess an image for the model."""
    transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)


def predict(model, image_tensor, device):
    """Make a prediction on an image."""
    image_tensor = image_tensor.to(device)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        top5_prob, top5_idx = torch.topk(probabilities, 5)

    return top5_idx[0].cpu().numpy(), top5_prob[0].cpu().numpy()


def main():
    """Main function."""
    print("=" * 60)
    print("Image Classification Example")
    print("=" * 60)

    # Set up device
    set_seed(42)
    device = get_device()

    # Load model (kept for demonstration purposes)
    _ = load_model(device)

    print("\n📝 Note: To use this example with a real image:")
    print("  1. Place an image in the examples/ folder")
    print("  2. Uncomment the prediction code below")
    print("  3. Replace 'your_image.jpg' with your image filename")

    # Example usage (uncomment when you have an image):
    # image_path = "examples/your_image.jpg"
    # image_tensor = preprocess_image(image_path)
    # top5_idx, top5_prob = predict(model, image_tensor, device)
    #
    # print("\nTop 5 Predictions:")
    # for idx, prob in zip(top5_idx, top5_prob):
    #     print(f"  Class {idx}: {prob*100:.2f}%")

    print("\n✅ Example completed!")


if __name__ == "__main__":
    main()
