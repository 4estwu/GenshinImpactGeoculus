import cv2
import sys

path = sys.argv[1]

#grayscale
img = cv2.imread(path)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#convert non-blacks to be white
(thresh, black_and_white_image) = cv2.threshold(gray_image, 15, 255, cv2.THRESH_BINARY)

height, width = black_and_white_image.shape

#invert it
inverted = ~black_and_white_image

cv2.imshow('image',black_and_white_image)
cv2.waitKey(0)

#connected components
#num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(grayImage, 8, cv2.CV_32S)
#print(centroids)
#tsp
