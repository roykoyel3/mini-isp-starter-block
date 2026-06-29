import cv2
import matplotlib.pyplot as plt
import numpy as np

import os

image_path = "results/input_images/Cat.jpeg"

img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Image not found!")
    exit()

# Extract filename without extension
image_name = os.path.splitext(os.path.basename(image_path))[0]

print(img.shape)


# 3x3 convolution kernel 

#Identity Kernel
identity_kernel = np.array([[0, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]])

identity_img = cv2.filter2D(img, -1, identity_kernel)

#Box Kernel
box_blur_kernel = np.array([[1/9, 1/9, 1/9],
                            [1/9, 1/9, 1/9],
                            [1/9, 1/9, 1/9]])

box_blur_img = cv2.filter2D(img, -1, box_blur_kernel)

#Gaussian Blur Kernel
gaussian_blur_kernel = np.array([[1/16, 2/16, 1/16],
                                [2/16, 4/16, 2/16],
                                [1/16, 2/16, 1/16]])

gaussian_blur_img = cv2.filter2D(img, -1, gaussian_blur_kernel)

# gaussian_blur_img = cv2.GaussianBlur(img, (5, 5), 1)

#Median Blur Kernel
median_blur_img = cv2.medianBlur(img, 5)

#Sharpen Kernel
sharpen_kernel = np.array([
    [ 0,-1, 0],
    [-1, 5,-1],
    [ 0,-1, 0]
], dtype=np.float32)

sharpen_img = cv2.filter2D(img, -1, sharpen_kernel)

#Emboss Kernel
emboss_kernel = np.array([
    [-2,-1, 0],
    [-1, 1, 1],
    [ 0, 1, 2]
], dtype=np.float32)

emboss_img = cv2.filter2D(img, -1, emboss_kernel)

#Sobel Kernels
sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
], dtype=np.float32)

sobel_y = np.array([
    [-1,-2,-1],
    [ 0, 0, 0],
    [ 1, 2, 1]
], dtype=np.float32) 

sobelx = cv2.filter2D(img, cv2.CV_64F, sobel_x)
sobely = cv2.filter2D(img, cv2.CV_64F, sobel_y)
sobelx_img = cv2.convertScaleAbs(sobelx)
sobely_img = cv2.convertScaleAbs(sobely)

#sobelx = cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
#sobely = cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)

# Display the results

plt.figure(figsize=(10, 6))

#Input Image
plt.subplot(3, 3, 1)
plt.imshow(img, cmap='gray')
plt.title("Input Image")
plt.axis("off")

# Identity Kernel
plt.subplot(3, 3, 2)
plt.imshow(identity_img, cmap='gray')
plt.title("Identity Kernel")
plt.axis("off")

# Box Blur Kernel
plt.subplot(3, 3, 3)
plt.imshow(box_blur_img, cmap='gray')
plt.title("Box Blur Kernel")
plt.axis("off")

# Gaussian Blur Kernel
plt.subplot(3, 3, 4)
plt.imshow(gaussian_blur_img, cmap='gray')
plt.title("Gaussian Blur Kernel")
plt.axis("off")

# Median Blur Kernel
plt.subplot(3, 3, 5)
plt.imshow(median_blur_img, cmap='gray')
plt.title("Median Blur Kernel")
plt.axis("off")

# Sharpen Kernel
plt.subplot(3, 3, 6)
plt.imshow(sharpen_img, cmap='gray')
plt.title("Sharpen Kernel")
plt.axis("off")

# Emboss Kernel
plt.subplot(3, 3, 7)
plt.imshow(emboss_img, cmap='gray')
plt.title("Emboss Kernel")
plt.axis("off")

# Sobel Kernels
plt.subplot(3, 3, 8)
plt.imshow(sobelx_img, cmap='gray')
plt.title('Sobel X - Vertical Edges')
plt.axis('off')

plt.subplot(3, 3, 9)
plt.imshow(sobely_img, cmap='gray')
plt.title('Sobel Y - Horizontal Edges')
plt.axis('off')

plt.show()


# Save Output Images

output_dir = f"results/output_images/{image_name}"

os.makedirs(output_dir, exist_ok=True)

cv2.imwrite(f"{output_dir}/identity.png", identity_img)
cv2.imwrite(f"{output_dir}/box_blur.png", box_blur_img)
cv2.imwrite(f"{output_dir}/gaussian_blur.png", gaussian_blur_img)
cv2.imwrite(f"{output_dir}/median_blur.png", median_blur_img)
cv2.imwrite(f"{output_dir}/sharpen.png", sharpen_img)
cv2.imwrite(f"{output_dir}/emboss.png", emboss_img)
cv2.imwrite(f"{output_dir}/sobel_x.png", sobelx_img)
cv2.imwrite(f"{output_dir}/sobel_y.png", sobely_img)

print(f"Output images saved in: {output_dir}")