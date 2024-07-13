import cv2
import numpy as np

from config.constants import BIRDS_EYE_MARGIN
from image_processing.plot_utils import plot_image


def apply_birds_eye(drone_img: np.array, coordinates):
    # L2 norm
    tl, tr, br, bl = coordinates[0], coordinates[1], coordinates[2], coordinates[3]
    # width
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    # height
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    # Destination points which will map the image to a bird's-eye view
    destination = np.array([[0, 0],
                            [max_width - 1, 0],
                            [max_width - 1, max_height - 1],
                            [0, max_height - 1]
                            ],
                           dtype="float32")
    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(np.array(coordinates, dtype="float32"), destination)
    # Apply the perspective transformation
    wrapped = cv2.warpPerspective(drone_img, M, (max_width, max_height))
    # If needed, crop the image to exclude boundary regions (adjust margin as needed)
    if BIRDS_EYE_MARGIN:
        wrapped = wrapped[BIRDS_EYE_MARGIN:max_height - BIRDS_EYE_MARGIN, BIRDS_EYE_MARGIN:max_width - BIRDS_EYE_MARGIN]
    return wrapped


def plot_birds_eye_view(birds_eye_img):
    image_rgb = cv2.cvtColor(birds_eye_img, cv2.COLOR_BGR2RGB)
    plot_image(image_rgb, "Bird's-Eye View")


def plot_path_on_birds_eye_image(birds_eye_img, direction_array, step_size):
    image_rgb = cv2.cvtColor(birds_eye_img, cv2.COLOR_BGR2RGB)
    x, y = (0, 0)
    path_coordinates = [((y + 1) * step_size, (x + 1) * step_size)]
    for order in direction_array:
        if order == 'Right':
            y += 1
        elif order == 'Down':
            x += 1
        elif order == 'Left':
            y -= 1
        elif order == 'Up':
            x -= 1
        path_coordinates.append(((y + 1) * step_size, (x + 1) * (step_size + 1)))
    for coord in path_coordinates:
        top_left = (coord[0] - step_size, coord[1] - step_size)
        bottom_right = (top_left[0] + step_size, top_left[1] + step_size)
        cv2.rectangle(image_rgb, top_left, bottom_right, color=(0, 255, 0), thickness=-1)
    plot_image(image_rgb, "Path Visualization")
