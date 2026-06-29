import cv2
import numpy as np
import os

# --------------------------------------------------
# Input Memory File
# --------------------------------------------------

mem_file = "results/memory_files/Cat.mem"
info_file = "results/memory_files/Cat_info.txt"

# --------------------------------------------------
# Read Image Dimensions
# --------------------------------------------------

with open(info_file, "r") as f:
    lines = f.readlines()

width = int(lines[0].split("=")[1])
height = int(lines[1].split("=")[1])

print(f"Image Size : {width} x {height}")

# --------------------------------------------------
# Read Memory File
# --------------------------------------------------

pixels = []

with open(mem_file, "r") as f:
    for line in f:
        pixels.append(int(line.strip(), 16))   # Hex → Decimal

pixels = np.array(pixels, dtype=np.uint8)

# --------------------------------------------------
# Reconstruct Image
# --------------------------------------------------

image = pixels.reshape((height, width))

# --------------------------------------------------
# Create Output Folder
# --------------------------------------------------

output_dir = "results/reconstructed_images"
os.makedirs(output_dir, exist_ok=True)

image_name = os.path.splitext(os.path.basename(mem_file))[0]

output_path = os.path.join(
    output_dir,
    f"{image_name}_reconstructed.png"
)

cv2.imwrite(output_path, image)

print(f"Reconstructed image saved as:\n{output_path}")

# --------------------------------------------------
# Display Image
# --------------------------------------------------

#cv2.imshow("Reconstructed Image", image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()