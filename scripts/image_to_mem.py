import cv2
import numpy as np
import os

# --------------------------------------------------
# Input Image
# --------------------------------------------------

image_path = "results/input_images/Cat.jpeg"

img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Error: Image not found!")
    exit()

# --------------------------------------------------
# Image Information
# --------------------------------------------------

height, width = img.shape

image_name = os.path.splitext(os.path.basename(image_path))[0]

print(f"Image Name : {image_name}")
print(f"Image Size : {width} x {height}")

# --------------------------------------------------
# Create Output Directory
# --------------------------------------------------

output_dir = "results/memory_files"
os.makedirs(output_dir, exist_ok=True)

mem_file = os.path.join(output_dir, f"{image_name}.mem")

# --------------------------------------------------
# Convert Image to Memory File
# --------------------------------------------------

pixels = img.flatten()

with open(mem_file, "w") as f:

    for pixel in pixels:
        f.write(f"{pixel:02X}\n")      # Hex format (00 - FF)

print(f"\nMemory file saved as:\n{mem_file}")

# --------------------------------------------------
# Save Image Dimensions
# --------------------------------------------------

info_file = os.path.join(output_dir, f"{image_name}_info.txt")

with open(info_file, "w") as f:
    f.write(f"WIDTH={width}\n")
    f.write(f"HEIGHT={height}\n")

print(f"Image information saved as:\n{info_file}")
