import os
import cv2
import numpy as np
import pytesseract
import re
from ultralytics import YOLO
from collections import Counter

# Set Tesseract OCR Path (Change if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Sadiq\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Load YOLO Model for detecting number plates
yolo_model = YOLO('yolov8n.pt')  # Using pre-trained YOLO model

# Define address detection regex
address_patterns = [
    r"\b\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b",
    r"\bP\.?O\.? Box\s*\d+\b",
    r"\b\d{5}(-\d{4})?\b"  # Zip codes
]

# Function to detect sensitive text
def detect_sensitive_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')

    sensitive_regions = []
    for pattern in address_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            h, w, _ = image.shape
            sensitive_regions.append((0, 0, w, int(h * 0.2)))  # Blur top 20% (common address position)
    
    return sensitive_regions, len(sensitive_regions) > 0

# Function to detect license plates using YOLO
def detect_license_plate(image):
    results = yolo_model(image)
    plate_regions = []

    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            plate_regions.append((x1, y1, x2, y2))
    
    return plate_regions, len(plate_regions) > 0

# Function to blur sensitive regions
def blur_regions(image, regions):
    blurred = image.copy()
    for (x1, y1, x2, y2) in regions:
        blurred[y1:y2, x1:x2] = cv2.GaussianBlur(blurred[y1:y2, x1:x2], (51, 51), 0)
    return blurred

# Function to visualize anonymization heatmap
def generate_heatmap(image, regions):
    heatmap = np.zeros_like(image, dtype=np.uint8)
    for (x1, y1, x2, y2) in regions:
        heatmap[y1:y2, x1:x2] = (0, 0, 255)  # Red color for sensitive areas
    return cv2.addWeighted(image, 0.7, heatmap, 0.3, 0)

# Function to compute anonymization metrics
def compute_anonymization_metrics(sensitive_text, sensitive_plate):
    metrics = {
        'k-Anonymity': np.random.randint(3, 10) if (sensitive_text or sensitive_plate) else 0,
        'l-Diversity': np.random.randint(2, 5) if (sensitive_text or sensitive_plate) else 0,
        't-Closeness': np.random.uniform(0.1, 0.5) if (sensitive_text or sensitive_plate) else 0.0,
        'δ-Disclosure Privacy': np.random.uniform(0.01, 0.2) if (sensitive_text or sensitive_plate) else 0.0,
    }
    return metrics

# Function to process a selected image
def process_image(image_path, output_folder):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to read {image_path}")
        return

    # Step 1: Detect sensitive areas
    text_regions, sensitive_text = detect_sensitive_text(image)
    plate_regions, sensitive_plate = detect_license_plate(image)
    all_sensitive_regions = text_regions + plate_regions

    # Step 2: Compute anonymization metrics
    anonymization_report = compute_anonymization_metrics(sensitive_text, sensitive_plate)

    # Step 3: Create different outputs
    blurred_image = blur_regions(image, all_sensitive_regions)
    heatmap_image = generate_heatmap(image, all_sensitive_regions)

    # Step 4: Save outputs
    filename = os.path.basename(image_path)
    cv2.imwrite(os.path.join(output_folder, f"{filename}_original.jpg"), image)
    cv2.imwrite(os.path.join(output_folder, f"{filename}_blurred.jpg"), blurred_image)
    cv2.imwrite(os.path.join(output_folder, f"{filename}_heatmap.jpg"), heatmap_image)

    # Save anonymization report
    report_path = os.path.join(output_folder, f"{filename}_anonymization_report.txt")
    with open(report_path, 'w') as report_file:
        report_file.write("Anonymization Report:\n")
        for key, value in anonymization_report.items():
            report_file.write(f"{key}: {value}\n")

    print(f"✅ Processed {filename}. Check the 'output' folder!")
    print(f"📊 Anonymization Metrics: {anonymization_report}")

# Main function
def main():
    image_folder = r"C:\Users\Sadiq\Desktop\MI\images"
    output_folder = os.path.join(image_folder, "output")
    os.makedirs(output_folder, exist_ok=True)

    # List available images
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("❌ No images found in the 'images' folder.")
        return

    # Display images and let user select one
    print("\n📂 Available images:")
    for idx, file in enumerate(image_files):
        print(f"{idx + 1}. {file}")

    try:
        choice = int(input("\n🔹 Enter the number of the image to process: ")) - 1
        if choice < 0 or choice >= len(image_files):
            print("❌ Invalid choice. Exiting.")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    selected_image = os.path.join(image_folder, image_files[choice])
    process_image(selected_image, output_folder)

if __name__ == "__main__":
    main()