from typing import List, Tuple
import numpy as np
import cv2
import matplotlib.pyplot as plt

from config.constants import BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, \
    BOUNDARIES_UPPER_BOUND2, OBSTACLES_UPPER_BOUND1, OBSTACLES_LOWER_BOUND1, DESTINATION_LOWER_BOUND1, \
    DESTINATION_UPPER_BOUND1, OBSTACLES_LOWER_BOUND2, OBSTACLES_UPPER_BOUND2, DESTINATION_UPPER_BOUND2, \
    DESTINATION_LOWER_BOUND2

"""def preprocess(image_path):
    # Load the image
    image = cv2.imread(image_path)
    boundaries = find_boundaries(image, BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, BOUNDARIES_UPPER_BOUND2)"""


def find_boundaries(image, lower_color1, upper_color1, lower_color2, upper_color2) -> List[Tuple[int, int]]:
    """
    Find points of a specific color range in the image using two sets of bounds.

    Parameters:
    - image: Input image in BGR format.
    - lower_color1: Lower bound of the first color range in HSV format.
    - upper_color1: Upper bound of the first color range in HSV format.
    - lower_color2: Lower bound of the second color range in HSV format.
    - upper_color2: Upper bound of the second color range in HSV format.

    Returns:
    - coordinates: List of coordinates of the detected points.
    """
    if image is None:
        raise ValueError("Image not loaded properly")

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create masks for the color ranges
    mask1 = cv2.inRange(hsv_image, lower_color1, upper_color1)
    mask2 = cv2.inRange(hsv_image, lower_color2, upper_color2)

    # Combine the masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the combined mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours to reduce noise
    min_contour_area = 100  # Adjust this value as needed
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) >= min_contour_area]

    # Get coordinates of the centers of the colored points
    coordinates = []
    for contour in filtered_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            coordinates.append((cX, cY))
    return coordinates


def order_boundaries(coordinates):
    coordinates = np.array(coordinates)
    # return [coordinates[3], coordinates[1], coordinates[0], coordinates[2]]
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
    # Convert the image from BGR to RGB for displaying with matplotlib
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_with_points = image.copy()

    # Draw circles at the specified coordinates
    for (x, y) in coordinates:
        cv2.circle(image_with_points, (x, y), 5, (0, 255, 0), -1)  # Green color

    # Display the image with matplotlib
    plt.figure(figsize=(10, 10))
    plt.imshow(image_with_points)
    plt.title("Input image with detected boundaries")
    plt.axis('off')  # Hide the axis
    plt.show()


def convert_birds_eye_to_matrix(image):
    """
    Processes the image to create a matrix with values 0, 1, and 2
    where 0 corresponds to the background, 1 to pink cubes, and 2 to blue cubes.

    Args:
    image_path (str): Path to the image file.

    Returns:
    np.ndarray: Matrix with values 0, 1, and 2.
    """
    # # Convert the image to RGB (OpenCV loads images in BGR format)
    # image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    #
    # # Convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image = image
    # Create masks for each color range
    obstacles_mask_1 = cv2.inRange(hsv_image, OBSTACLES_LOWER_BOUND1, OBSTACLES_UPPER_BOUND1)
    obstacles_mask_2 = cv2.inRange(hsv_image, OBSTACLES_LOWER_BOUND2, OBSTACLES_UPPER_BOUND2)
    obstacles_mask = cv2.bitwise_or(obstacles_mask_1, obstacles_mask_2)
    destination_mask_1 = cv2.inRange(hsv_image, DESTINATION_LOWER_BOUND1, DESTINATION_UPPER_BOUND1)
    destination_mask_2 = cv2.inRange(hsv_image, DESTINATION_LOWER_BOUND2, DESTINATION_UPPER_BOUND2)
    destination_mask = cv2.bitwise_or(destination_mask_1, destination_mask_2)

    boundaries_mask_1 = cv2.inRange(hsv_image, BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1)
    boundaries_mask_2 = cv2.inRange(hsv_image, BOUNDARIES_LOWER_BOUND2, BOUNDARIES_UPPER_BOUND2)
    boundaries_mask = cv2.bitwise_or(boundaries_mask_1, boundaries_mask_2)

    # Initialize the matrix with zeros (for background)
    matrix = np.zeros(image.shape[:2], dtype=int)

    # Set matrix values based on masks
    matrix[obstacles_mask > 0] = 1
    matrix[destination_mask > 0] = 2
    matrix[boundaries_mask > 0] = 2
    return matrix


def save_and_display_matrix(matrix, output_image_path):
    """
    Saves the matrix as an image and displays it.
    
    Args:
    matrix (np.ndarray): Matrix with values 0, 1, and 2.
    output_image_path (str): Path to save the output image.
    """
    # Save the matrix as an image
    # plt.imsave(output_image_path, matrix, cmap='viridis')

    # Display the matrix as an image
    plt.imshow(matrix, cmap='viridis')
    plt.colorbar(ticks=[0, 1, 2], label='Color Code')
    plt.title('Color-Coded Matrix')
    plt.show()

    # Print the result matrix
    print("Result Matrix:")
    print(matrix)
