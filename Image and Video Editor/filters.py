import cv2 as cv
import numpy as np

# Load the image
image = cv.imread('input_image5.png')

# Convert the image to grayscale
gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Negate the grayscale image
# negated_image = cv.bitwise_not(gray_image)

#log
# c = 1
# log_transformed_image = c * np.log1p(gray_image)

# # Scale the result to the range [0, 255]
# scaled_image = ((log_transformed_image - log_transformed_image.min()) / (log_transformed_image.max() - log_transformed_image.min()) * 255).astype(np.uint8)

#power
# c = 1
# g = 3.0

# # Apply the power-law transformation
# transformed_image = c * np.power(gray_image, g)

# # Scale the result to the range [0, 255]
# scaled_image = ((transformed_image - transformed_image.min()) / (transformed_image.max() - transformed_image.min()) * 255).astype(np.uint8)

#piecewise
# def piecewise_linear(x):
#     if 0 <= x < 50:
#         return 0
#     elif 50 <= x < 100:
#         return 5 * (x - 50)
#     elif 100 <= x < 150:
#         return 10 * (x - 100) + 250
#     elif 150 <= x < 200:
#         return 5 * (x - 150) + 500
#     else:
#         return 255

# # Apply the piecewise linear transformation to the image
# transformed_image = np.vectorize(piecewise_linear)(gray_image).astype(np.uint8)

#gaussianBlur
filtered_image1 = cv.GaussianBlur(gray_image, (43, 43), 7)

# Display the original and negated images
cv.imshow('Original Image', image)
cv.imshow('Negated Image', filtered_image1)
cv.waitKey(0)
cv.destroyAllWindows()
