from typing import List, Tuple
import numpy as np
import cv2

from config.constants import BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, \
    BOUNDARIES_UPPER_BOUND2, OBSTACLES_UPPER_BOUND1, OBSTACLES_LOWER_BOUND1, DESTINATION_LOWER_BOUND1, \
    DESTINATION_UPPER_BOUND1, OBSTACLES_LOWER_BOUND2, OBSTACLES_UPPER_BOUND2, DESTINATION_UPPER_BOUND2, \
    DESTINATION_LOWER_BOUND2, MIN_CONTOUR_AREA
from image_processing.plot_utils import plot_image


def _get_mask_by_two_hsv_color_ranges(image, lower_bound_1, upper_bound_1, lower_bound_2, upper_bound_2):
    mask_1 = cv2.inRange(image, lower_bound_1, upper_bound_1)
    mask_2 = cv2.inRange(image, lower_bound_2, upper_bound_2)
    unified_mask = cv2.bitwise_or(mask_1, mask_2)
    return unified_mask


def _get_center_coordinate_of_contour(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        return x, y


def find_boundaries(image, lower_color_1, upper_color_1, lower_color_2, upper_color_2) -> List[Tuple[int, int]]:
    """
    Find points of a specific color range in the image using two sets of bounds.

    Parameters:
    - image: Input image in BGR format.
    - lower_color_1: Lower bound of the first color range in HSV format.
    - upper_color_1: Upper bound of the first color range in HSV format.
    - lower_color_2: Lower bound of the second color range in HSV format.
    - upper_color_2: Upper bound of the second color range in HSV format.

    Returns:
    - coordinates: List of coordinates of the detected points.
    """
    if image is None:
        raise ValueError("Image not loaded properly")
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = _get_mask_by_two_hsv_color_ranges(image=hsv_image,
                                             lower_bound_1=lower_color_1,
                                             upper_bound_1=upper_color_1,
                                             lower_bound_2=lower_color_2,
                                             upper_bound_2=upper_color_2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filter out small contours to reduce noise
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) >= MIN_CONTOUR_AREA]
    # Get coordinates of the centers of the colored points
    coordinates = []
    for contour in filtered_contours:
        x, y = _get_center_coordinate_of_contour(contour)
        if x:
            coordinates.append((x, y))
    return coordinates


def order_boundaries(coordinates):
    """
    Order the coordinates of the navigation plane boundaries to align with the birds eye algorithm requirements
    """
    coordinates = np.array(coordinates)
    rect = np.zeros((4, 2), dtype="float32")
    # Sum of points
    s = coordinates.sum(axis=1)
    rect[0] = coordinates[np.argmin(s)]
    rect[2] = coordinates[np.argmax(s)]
    # Difference of points
    diff = np.diff(coordinates, axis=1)
    rect[1] = coordinates[np.argmin(diff)]
    rect[3] = coordinates[np.argmax(diff)]
    return rect


def plot_img_with_boundaries(image, coordinates):
    # TODO - check if the conversion line is required or not at uni
    # Convert the image from BGR to RGB for displaying with matplotlib
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_with_points = image.copy()
    # Draw circles at the specified coordinates
    for (x, y) in coordinates:
        cv2.circle(image_with_points, (x, y), 5, (0, 255, 0), -1)  # Green color
    # Display the image with matplotlib
    plot_image(image_with_points, "Input image with detected boundaries")


def convert_birds_eye_image_to_matrix(image):
    """
    Processes the image to create a matrix with values 0, 1, and 2
    where 0 corresponds to the background, 1 to obstacles and 2 to destination.
    Returns:
    np.ndarray: Matrix with values 0, 1, and 2.
    """
    # # Convert the image to RGB and then to HSV which suits best for color ranges (OpenCV loads images in BGR format)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # Get Color masks
    obstacles_mask = _get_mask_by_two_hsv_color_ranges(hsv_image,
                                                       lower_bound_1=OBSTACLES_LOWER_BOUND1,
                                                       upper_bound_1=OBSTACLES_UPPER_BOUND1,
                                                       lower_bound_2=OBSTACLES_LOWER_BOUND2,
                                                       upper_bound_2=OBSTACLES_UPPER_BOUND2
                                                       )
    destination_mask = _get_mask_by_two_hsv_color_ranges(hsv_image,
                                                         lower_bound_1=DESTINATION_LOWER_BOUND1,
                                                         upper_bound_1=DESTINATION_UPPER_BOUND1,
                                                         lower_bound_2=DESTINATION_LOWER_BOUND2,
                                                         upper_bound_2=DESTINATION_UPPER_BOUND2
                                                         )
    boundaries_mask = _get_mask_by_two_hsv_color_ranges(hsv_image,
                                                        lower_bound_1=BOUNDARIES_LOWER_BOUND1,
                                                        upper_bound_1=BOUNDARIES_UPPER_BOUND1,
                                                        lower_bound_2=BOUNDARIES_LOWER_BOUND2,
                                                        upper_bound_2=BOUNDARIES_UPPER_BOUND2
                                                        )
    # Initialize the matrix with zeros (for background)
    birds_eye_matrix = np.zeros(image.shape[:2], dtype=int)
    # Set matrix values based on masks
    birds_eye_matrix[boundaries_mask > 0] = 0
    birds_eye_matrix[obstacles_mask > 0] = 1
    birds_eye_matrix[destination_mask > 0] = 2
    return birds_eye_matrix
