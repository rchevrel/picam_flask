import cv2
import numpy as np

def showImage(img):
    cv2.imshow("original", img)
    cv2.waitKey()
    cv2.imshow("canny", cv2.Canny(img, 200, 100))
    cv2.waitKey()
    cv2.destroyAllWindows()

showImage(cv2.imread("line_detector/images/slide_01.jpg", 0))
showImage(cv2.imread("line_detector/images/slide_02.jpg", 0))
showImage(cv2.imread("line_detector/images/slide_03.jpg", 0))
showImage(cv2.imread("line_detector/images/slide_04.jpg", 0))
showImage(cv2.imread("line_detector/images/slide_05.jpg", 0))
showImage(cv2.imread("line_detector/images/slide_06.jpg", 0))
