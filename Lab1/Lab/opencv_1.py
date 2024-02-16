import cv2 as cv
import numpy as np

print(cv.__version__)
image = cv.imread("landscape.jpg")
print(image.shape)
# print(image[:,:,0])

image1 = image[:,0:100,:]
image[:,-100:,:] =image1

# z = np.zeros([159,199])
# image1[:,:,0] = z
# image1[:,:,1] = z
# image2 = image[:,:,1]
# image3 = image[:,:,2]
cv.imshow("1",image)
# cv.imshow("2",image2)
# cv.imshow("3",image3)
cv.waitKey()