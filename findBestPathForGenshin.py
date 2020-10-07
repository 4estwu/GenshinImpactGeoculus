import cv2

path = '/mnt/e/genshinGeoculusMap.jpg'

#grayscale
img = cv2.imread(path)
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#convert non-blacks to be white
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 15, 255, cv2.THRESH_BINARY)

height, width, ___ = img.shape

#invert it
for row in range(0, height - 1):
    for col in range(0, width -1 ):
        pixel = img[row, col] 
        for val in pixel:
            val = 255 - val
        
        img[row, col] = pixel 

cv2.imshow('image',img)

#tsp
