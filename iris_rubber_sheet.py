import sys
import cv2
import numpy as np
from scipy.interpolate import interp1d
from PIL import Image

from daugman import find_iris


def generate_rubber_sheet_model(img, save_filename):
    q = np.arange(0.00, np.pi * 2, 0.01)  # theta
    inn = np.arange(0, int(img.shape[0] / 2), 1)  # radius

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
    im = Image.fromarray(cartisian_image)
    im.save(save_filename)


def daugman_method(
    image_path, localized, rubber_sheet, is_gray=True, high_contrast=False
):
    img_opened = np.asarray(Image.open(image_path))
    iris_localized = img_opened.copy()

    if not is_gray:
        img_opened = cv2.cvtColor(img_opened, cv2.COLOR_BGR2GRAY)

    if high_contrast:
        img_opened = cv2.equalizeHist(img_opened)

    iris_coordinates, r = find_iris(
        img_opened, daugman_start=70, daugman_end=150, daugman_step=5, points_step=3
    )

    print(iris_coordinates, r)

    x = int(iris_coordinates[0])
    y = int(iris_coordinates[1])

    h, w = r, r

    cv2.circle(iris_localized, iris_coordinates, r, (255, 0, 0), thickness=1)
    cv2.circle(iris_localized, iris_coordinates, 4, (255, 255, 0), thickness=1)
    im = Image.fromarray(iris_localized)
    im.save(localized)

    iris_image = img_opened[y - h : y + h, x - w : x + w]
    iris = cv2.resize(iris_image, (iris_image.shape[1] * 2, iris_image.shape[0] * 2))

    im = Image.fromarray(iris)
    im.save("iris.jpg")

    generate_rubber_sheet_model(iris_image, rubber_sheet)


input_image = sys.argv[1]
localized = sys.argv[2]
rubber_sheet = sys.argv[3]

# daugman_method(
#     input_image,
#     "iris_localized.jpg",
#     "iris_rubber_sheet.jpg",
#     is_gray=True,
#     high_contrast=False,
# )

daugman_method(
    input_image,
    localized,
    rubber_sheet,
    is_gray=True,
    high_contrast=False,
)
