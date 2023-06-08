import sys
import cv2
import numpy as np

from scipy.interpolate import interp1d
from PIL import Image
from utils import *


def generate_rubber_sheet_model(img, save_filename):
    q = np.arange(0.00, np.pi * 2, 0.01)
    inn = np.arange(0, int(img.shape[0] / 2), 1)

    cartisian_image = np.empty(shape=[inn.size, int(img.shape[1]), 3])
    m = interp1d([np.pi * 2, 0], [0, img.shape[1]])

    for r in inn:
        for t in q:
            polarX = int((r * np.cos(t)) + img.shape[1] / 2)
            polarY = int((r * np.sin(t)) + img.shape[0] / 2)
            try:
                cartisian_image[r][int(m(t) - 1)] = img[polarY][polarX]
            except:
                pass

    cartisian_image = cartisian_image.astype("uint8")
    save_img(cartisian_image, save_filename)


def remove_reflection(img):
    ret, mask = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=1)
    dst = cv2.inpaint(img, dilation, 5, cv2.INPAINT_TELEA)
    return dst


def processing(image_path, r):
    success = False
    image = cv2.imread(image_path)
    image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_LINEAR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(image, 11)
    ret, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1,
        50,
        param1=ret,
        param2=30,
        minRadius=20,
        maxRadius=100,
    )
    try:
        circles = circles[0, :, :]
        circles = np.int16(np.array(circles))
        for i in circles[:]:
            image = image[
                i[1] - i[2] - r : i[1] + i[2] + r, i[0] - i[2] - r : i[0] + i[2] + r
            ]
            radius = i[2]
        success = True
        return image, radius, success
    except:
        image[:] = 255
        print(f"{image_path} -> No circles (iris) found.")
        success = False
        return image, image.shape[0], success


def process_img(
    filename, iris_save_filename, rs_save_filename, keep_reflection=False
):

    image_roi, rr, success = processing(filename, 50)

    if success:
        if not keep_reflection:
            image_roi = remove_reflection(image_roi)

        save_img(image_roi, iris_save_filename)
        generate_rubber_sheet_model(image_roi, rs_save_filename)
    else:
        pass


if __name__ == "__main__":
    img_filename = sys.argv[1]
    iris_save_filename = sys.argv[2]
    rs_save_filename = sys.argv[3]
    process_img(img_filename, iris_save_filename, rs_save_filename)
