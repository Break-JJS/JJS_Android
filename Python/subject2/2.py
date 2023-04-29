# try:
#     from cv2 import cv2
# except ImportError:
#     pass
import math

import cv2

def setLabel(img, pts, label):
    (x, y, w, h) = cv2.boundingRect(pts)
    pt1 = (x, y)
    pt2 = (x+w, y+h)
    cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)
    cv2.putText(img, label, pt1, cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

def main():
    src = cv2.imread('src/case2/img2_1.png', cv2.IMREAD_COLOR)

    if src is None:
        print('Image load failed!')
        return

    gray = ~cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    idx = 0
    for pts in contours:
        idx += 1
        if cv2.contourArea(pts) < 400:
            continue

        approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True)*0.02, True)

        vtc = len(approx)
        print(f'{vtc}')

        if vtc == 3:
            setLabel(src, pts, 'TRI')
        elif vtc == 4:
            setLabel(src, pts, 'RECT')

            (x, y, w, h) = cv2.boundingRect(pts)
            img_tmp = img_bin[y:y+h, x:x+w]

            blurred = cv2.blur(img_tmp, (3, 3))
            circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 5, param1=150, param2=10, minRadius=0, maxRadius=10)

            dst = cv2.cvtColor(img_tmp, cv2.COLOR_GRAY2BGR)

            if circles is not None:
                print(f'Circles: {circles.shape[1]}')
                for i in range(circles.shape[1]):
                    cx, cy, radius = circles[0][i]
                    cv2.circle(dst, (int(cx), int(cy)), int(radius), (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow(f'dst{idx}', dst)

        else:
            lenth = cv2.arcLength(pts, True)
            area = cv2.contourArea(pts)
            ratio = 4. * math.pi * area / (lenth * lenth)

            if ratio > 0.85:
                setLabel(src, pts, 'CIR')

    cv2.imshow('src', src)
    cv2.imshow('img_bin', img_bin)
    cv2.waitKey()
    cv2.destroyAllWindows()

main()
