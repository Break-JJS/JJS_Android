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
    print('asd')

    src = cv2.imread('src/case3/img3_3.png', cv2.IMREAD_GRAYSCALE)

    if src is None:
        print('Image load failed!')
        return

    bsize = 151
    alpha = 2.0

    src_blur = cv2.GaussianBlur(src, (3, 3), 6)
    src_sharp = ~cv2.addWeighted(src, 1+alpha, src_blur, -alpha, 0.0)

    src_bin = cv2.adaptiveThreshold(src_sharp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, bsize, 7)
    src_med = cv2.medianBlur(src_bin, 5)
    dst = cv2.morphologyEx(src_med, cv2.MORPH_CLOSE, None, iterations=2)
    dst = cv2.medianBlur(dst, 15)

    dst = ~cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    gray = ~cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    idx = 0
    for pts in contours:
        idx += 1
        if cv2.contourArea(pts) < 400:
            continue

        approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True)*0.15, True)

        vtc = len(approx)
        print(f'{vtc}')

        if vtc == 3:
            setLabel(dst, pts, 'TRI')
        elif vtc == 4:
            setLabel(dst, pts, 'RECT')

            (x, y, w, h) = cv2.boundingRect(pts)
            img_tmp = img_bin[y:y+h, x:x+w]

            blurred = cv2.blur(img_tmp, (3, 3))
            circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 10, param1=160, param2=10, minRadius=8, maxRadius=15)

            img_dst = cv2.cvtColor(img_tmp, cv2.COLOR_GRAY2BGR)

            if circles is not None:
                print(f'Circles: {circles.shape[1]}')
                for i in range(circles.shape[1]):
                    cx, cy, radius = circles[0][i]
                    cv2.circle(img_dst, (int(cx), int(cy)), int(radius), (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow(f'dst{idx}', img_dst)

        else:
            lenth = cv2.arcLength(pts, True)
            area = cv2.contourArea(pts)
            ratio = 4. * math.pi * area / (lenth * lenth)

            if ratio > 0.85:
                setLabel(dst, pts, 'CIR')

    cv2.imshow('dst', dst)
    # cv2.imshow('src_med', src_med)
    # cv2.imshow('src_bin', src_bin)
    # cv2.imshow('src_sharp', src_sharp)
    # cv2.imshow('src_blur', src_blur)
    cv2.imshow('src', src)

    cv2.waitKey()
    cv2.destroyAllWindows()


main()
