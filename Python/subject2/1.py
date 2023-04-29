# try:
#     from cv2 import cv2
# except ImportError:
#     pass
import cv2

def hough_circles():
    src = cv2.imread('src/case1/img1_4.png', cv2.IMREAD_GRAYSCALE)

    if src is None:
        print('Image load failed!')
        return

    blurred = cv2.blur(src, (3, 3))
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 5, param1=150, param2=30)

    dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

    if circles is not None:
        print(f'Circles: {circles.shape[1]}')
        for i in range(circles.shape[1]):
            cx, cy, radius = circles[0][i]
            cv2.circle(dst, (int(cx), int(cy)), int(radius), (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('src', src)
    cv2.imshow('dst', dst)
    cv2.waitKey()
    cv2.destroyAllWindows()

hough_circles()
