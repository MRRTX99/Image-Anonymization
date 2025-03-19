# Image Anonymization Project

## 📌 Overview
This project is designed to **automatically detect and anonymize** sensitive information in images using **OCR (Optical Character Recognition), Object Detection, and Anonymization Algorithms**. It detects and blurs sensitive text (such as addresses and phone numbers) and license plates in images while preserving the original image for reference.

The anonymization techniques used include:
- **k-Anonymity**
- **l-Diversity**
- **t-Closeness**
- **δ-Disclosure Privacy**

The system also generates a **heatmap visualization** to highlight detected sensitive areas before applying anonymization.

---

## 💂️ Project Structure
```
Image-Anonymization-Project/
│── images/                      # Folder containing input images
│   ├── image1.jpg               # Example input image
│   ├── image2.jpg               
│── output/                      # Output folder for anonymized images
│   ├── image1_original.jpg      # Original image
│   ├── image1_blurred.jpg       # Anonymized output
│   ├── image1_heatmap.jpg       # Heatmap showing detected sensitive areas
│── main.py                      # Main script for processing images
│── README.md                    # Project documentation
```

---

## 💝 Installation & Setup

### 🔹 Step 1: Install Dependencies
Ensure you have **Python 3.8+** installed. Then, install the required packages:
```bash
pip install opencv-python numpy pytesseract ultralytics
```

### 🔹 Step 2: Install Tesseract OCR
Download and install **Tesseract OCR** from [here](https://github.com/UB-Mannheim/tesseract/wiki). Keep the default installation path (or note it down for later configuration).

After installation, update the script with your Tesseract path:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Path\to\Tesseract-OCR\tesseract.exe'
```

### 🔹 Step 3: Download YOLO Model
This project uses the **YOLOv8 model** for license plate detection. Download the pre-trained weights:
```bash
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Ensure this file is available
```

---

## 🚀 Usage

### 1️⃣ Place Images in the `images/` Folder
Copy the images you want to process into the `images` directory.

### 2️⃣ Run the Script
Execute the script using:
```bash
python main.py
```

### 3️⃣ Select an Image
The script will list all available images and prompt you to select one:
```
📂 Available images:
1. image1.jpg
2. image2.jpg
🔹 Enter the number of the image to process: 1
```

### 4️⃣ Output Files
Once processing is complete, the following files will be generated inside the `output/` folder:
- **image_original.jpg** → Unmodified original image
- **image_blurred.jpg** → Image with detected sensitive areas blurred
- **image_heatmap.jpg** → Heatmap showing detected sensitive areas before blurring

---

## 🛠️ How It Works

### 🔍 Step 1: Detect Sensitive Information
The project uses **OCR (Tesseract)** and **YOLOv8 Object Detection** to find:
- Addresses, phone numbers, and sensitive text using **Regex patterns & OCR**
- License plates using **YOLOv8 model**

### 🎭 Step 2: Apply Anonymization
After detection, the system applies:
- **Blurring** of identified regions using Gaussian Blur.
- **Heatmap visualization** for detected sensitive areas.

### 📊 Step 3: Anonymization Technique Evaluation
The anonymization techniques are measured and logged:
| Technique           | Description | Implementation in Code |
|---------------------|-------------|------------------------|
| **k-Anonymity**    | Ensures each record is indistinguishable from at least `k-1` others | Applied to group similar sensitive elements |
| **l-Diversity**    | Extends k-anonymity by ensuring diversity in sensitive values | Checks multiple occurrences of sensitive terms |
| **t-Closeness**    | Maintains statistical closeness of data to the original | Measures variance between original and anonymized text |
| **δ-Disclosure Privacy** | Limits an attacker's ability to infer sensitive values | Restricts exposure probability |

These anonymization metrics are printed in the console after processing.

---



## 📚 License
This project is open-source and licensed under the MIT License.

