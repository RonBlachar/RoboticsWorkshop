import cv2
import numpy as np


def get_drone_img(image_path) -> np.array:
    image = cv2.imread(image_path)


