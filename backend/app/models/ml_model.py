import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a smaller set of classes if imagenet_classes.json is not available
DEFAULT_CLASSES = {
    str(i): f"class_{i}" for i in range(1000)
}

# Load the pretrained model
try:
    model = models.resnet50(pretrained=True)
    model.eval()
    logger.info("ResNet50 model loaded successfully")
except Exception as e:
    logger.error(f"Error loading ResNet50 model: {str(e)}")
    # Fallback to a smaller model if ResNet50 fails
    try:
        logger.info("Trying to load ResNet18 instead...")
        model = models.resnet18(pretrained=True)
        model.eval()
    except Exception as e:
        logger.error(f"Error loading fallback model: {str(e)}")
        raise

# Try to load ImageNet class labels
try:
    # Check if file exists in absolute path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'imagenet_classes.json')
    
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            IMAGENET_CLASSES = json.load(f)
            logger.info(f"Loaded ImageNet classes from {json_path}")
    else:
        # Try relative path from execution directory
        alternative_path = 'app/models/imagenet_classes.json'
        if os.path.exists(alternative_path):
            with open(alternative_path, 'r') as f:
                IMAGENET_CLASSES = json.load(f)
                logger.info(f"Loaded ImageNet classes from {alternative_path}")
        else:
            logger.warning("ImageNet classes file not found, using default classes")
            IMAGENET_CLASSES = DEFAULT_CLASSES
except Exception as e:
    logger.error(f"Error loading ImageNet classes: {str(e)}")
    IMAGENET_CLASSES = DEFAULT_CLASSES

# Image transformation pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def get_prediction(image_bytes):
    """
    Get prediction from image bytes
    """
    try:
        # Convert image bytes to PIL image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert non-RGB images to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Apply transformations and add batch dimension
        image_tensor = transform(image).unsqueeze(0)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted = torch.max(outputs, 1)
            
        # Get class name and probability
        class_idx = predicted.item()
        class_name = IMAGENET_CLASSES.get(str(class_idx), f"class_{class_idx}")
        
        # Get top 5 predictions
        probs, indices = torch.topk(torch.nn.functional.softmax(outputs, dim=1), 5)
        
        results = []
        for i in range(5):
            idx = indices[0][i].item()
            results.append({
                "class": IMAGENET_CLASSES.get(str(idx), f"class_{idx}"),
                "probability": float(probs[0][i].item())
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        raise Exception(f"Prediction error: {str(e)}")