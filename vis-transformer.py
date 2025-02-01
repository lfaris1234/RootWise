from ultralytics import YOLO
import cv2
import numpy as np
import os

# Load YOLO model
model = YOLO("best.pt") 

# Load and check image
image_path = "images/image.jpg"
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image not found at: {image_path}")

img = cv2.imread(image_path)
if img is None:
    raise ValueError("Failed to load image. Check the file path and format.")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Run YOLO model
results = model(img, imgsz=1280)

# Print all detected objects
# print("RAW OUTPUT:", results[0].boxes)

# Get class indices and confidence scores
class_indices = results[0].boxes.cls.cpu().numpy() if results[0].boxes.cls is not None else np.array([])
confidence_scores = results[0].boxes.conf.cpu().numpy() if results[0].boxes.conf is not None else np.array([])

# Convert indices to labels (Safeguarded)
if class_indices.size > 0:
    class_labels = [model.names[int(idx)] for idx in class_indices]
else:
    class_labels = []

# Print detected classes and confidence scores
print("All Detected Objects:", list(zip(class_labels, confidence_scores)))

# Define vegetable labels
vegetable_labels = {
    "broccoli", "carrot", "cauliflower", "cucumber", "lettuce",
    "onion", "bell pepper", "potato", "spinach", "tomato", "zucchini",
    "green pepper", "red pepper", "jalapeno", "eggplant", "radish"
}

# Print all detected objects before filtering
for label, score in zip(class_labels, confidence_scores):
    print(f"Detected: {label} (Confidence: {score:.2f})")

# Filter detected vegetables with lower confidence threshold
threshold = 0.05
identified_vegetables = [
    label for label, score in zip(class_labels, confidence_scores)
    if label in vegetable_labels and score > threshold
]

print("Identified Vegetables:", identified_vegetables)
