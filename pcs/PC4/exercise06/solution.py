import cv2
import numpy as np
import torch
from torchvision import transforms
from torchvision.models.detection import yolo_v7
from segment_anything import SamPredictor, sam_model_registry


def load_yolo_model():
    model = yolo_v7(pretrained=True)
    model.eval()
    return model


def load_sam_model():
    sam = sam_model_registry["vit_h"](pretrained=True)  # Assuming 'vit_h' is the desired variant
    predictor = SamPredictor(sam)
    return predictor


def highlight_people_cars_and_bikes(
    full_path_input_image,
    color_scale_image,
    color_scale_people,
    color_scale_cars,
    color_scale_bikes,
    full_path_output_image
):
    # Load models
    yolo_model = load_yolo_model()
    sam_predictor = load_sam_model()
    
    # Load image
    image = cv2.imread(full_path_input_image)
    original_image = image.copy()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert image to desired color scale
    image[:] = color_scale_image
    
    # Preprocess the image for YOLO
    transform = transforms.Compose([transforms.ToTensor()])
    img_tensor = transform(image_rgb).unsqueeze(0)
    
    # Perform YOLO detection
    with torch.no_grad():
        predictions = yolo_model(img_tensor)[0]
    
    # Set up SAM predictor
    sam_predictor.set_image(image_rgb)
    
    # Parse predictions and apply SAM segmentation
    for i in range(len(predictions["labels"])):
        label = predictions["labels"][i].item()
        score = predictions["scores"][i].item()
        if score >= 0.5:  # Confidence threshold
            bbox = predictions["boxes"][i].cpu().numpy().astype(int)
            # Get mask from SAM
            masks, _, _ = sam_predictor.predict(bbox)
            
            if label == 0:  # Person
                color = color_scale_people
            elif label == 1:  # Bike
                color = color_scale_bikes
            elif label == 2:  # Car
                color = color_scale_cars
            else:
                continue
            
            # Apply the color to the mask region
            for j in range(3):
                image[:, :, j][masks == 1] = color[j]
    
    # Save the output image
    cv2.imwrite(full_path_output_image, image)

# # Example usage
# full_path_input_image = '/home/someone/example-1.jpg'
# color_scale_image = (255, 255, 255)
# color_scale_people = (255, 0, 0)
# color_scale_cars = (0, 255, 0)
# color_scale_bikes = (0, 0, 255)
# full_path_output_image = '/home/someone/detections-example-1.jpg'

# highlight_people_cars_and_bikes(
#     full_path_input_image,
#     color_scale_image,
#     color_scale_people,
#     color_scale_cars,
#     color_scale_bikes,
#     full_path_output_image
# )
