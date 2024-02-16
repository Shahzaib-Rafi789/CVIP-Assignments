import cv2 as cv
import numpy as np

image = cv.imread(r'C:\Users\PMLS\Desktop\Semester 6\CVIP LAB\Lab1\Home\collage.jpg')

if image is not None:
    height, width = image.shape[0], image.shape[1]
    print(image.shape)
else:
    print("Failed to read the image.")

newHeight = height // 3
print(newHeight)

cropedImage = image[0:newHeight, :, :]
# cv.imshow("Croped", cropedImage)

partitionwidth = width // 9
partition1 = cropedImage[:, :partitionwidth, :]
partition2 = cropedImage[:, partitionwidth*4:partitionwidth*5, :]
partition3 = cropedImage[:, partitionwidth*8:, :]

# print(partition1.shape)
# print(partition2.shape)

collage = np.concatenate((partition1, partition2, partition3), axis=1)
cv.imshow("Collage", collage)

cv.waitKey()
cv.destroyAllWindows()
