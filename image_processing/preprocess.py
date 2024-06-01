from typing import List, Tuple
import numpy as np
import cv2
import matplotlib.pyplot as plt

from config.constants import BOUNDARIES_LOWER_BOUND, BOUNDARIES_UPPER_BOUND, OBSTACLES_UPPER_BOUND, \
    OBSTACLES_LOWER_BOUND, DESTINATION_LOWER_BOUND, DESTINATION_UPPER_BOUND


def preprocess(image_path):
    # Load the image
    image = cv2.imread(image_path)
    boundaries = find_boundaries(image, BOUNDARIES_LOWER_BOUND, BOUNDARIES_UPPER_BOUND)



def find_boundaries(image, lower_color, upper_color) -> List[Tuple[int, int]]:
    """
    Find points of a specific color range in the image.
    
    Parameters:
    - image: Input image in BGR format.
    - lower_color: Lower bound of the color in HSV format.
    - upper_color: Upper bound of the color in HSV format.
    
    Returns:
    - coordinates: List of coordinates of the detected points.
    """
    if image is None:
        raise ValueError("Image not loaded properly")

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create mask for the color range
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Find contours in the mask
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
    # return [coordinates[1], coordinates[3], coordinates[2], coordinates[0]]
    return [coordinates[3], coordinates[1], coordinates[0], coordinates[2]]


def boundaries_process_image(image, lower_color, upper_color, output_image_path):
    # Find the colored points in the image
    coordinates = find_boundaries(image, lower_color, upper_color)
    print("Detected coordinates:", coordinates)

    # Draw the detected points on the image
    for (x, y) in coordinates:
        cv2.circle(image, (x, y), 10, (255, 0, 0), -1)  # Blue circles for detected points

    # Save the output image
    cv2.imwrite(output_image_path, image)

    # Display the image with marked points (optional)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.title("Detected Colored Points")
    plt.show()

    print(f"Output image saved at: {output_image_path}")


def process_image(image):
    """
    Processes the image to create a matrix with values 0, 1, and 2
    where 0 corresponds to the background, 1 to pink cubes, and 2 to blue cubes.
    
    Args:
    image_path (str): Path to the image file.
    
    Returns:
    np.ndarray: Matrix with values 0, 1, and 2.
    """
    # Convert the image to RGB (OpenCV loads images in BGR format)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Create masks for each color range
    obstacles_mask = cv2.inRange(hsv_image, OBSTACLES_LOWER_BOUND, OBSTACLES_UPPER_BOUND)
    destination_mask = cv2.inRange(hsv_image, DESTINATION_LOWER_BOUND, DESTINATION_UPPER_BOUND)

    # Initialize the matrix with zeros (for background)
    matrix = np.zeros(image.shape[:2], dtype=int)

    # Set matrix values based on masks
    matrix[obstacles_mask > 0] = 1
    matrix[destination_mask > 0] = 2

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


if __name__ == "__main__":
    """# ========================================= Start: Get_boundries() testing here =================================
    # Load the test image
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    process_image('testing_data/images/input_image.jpeg', lower_blue, upper_blue, 'testing_data/images/output_image.png')
    # ========================================= End: Get_boundries() testing here ================================="""

    """
    #========================================== convert matrix to 0/1/2 value ====================================
    # Path to the image file
    image_path = 'testing_data/images/projection_test.jpeg'
    
    # Path to save the output image
    output_image_path = 'testing_data/images/output_matrix_image.png'
    
    # Process the image and get the matrix
    matrix = process_image(image_path)
    
    # Save and display the matrix
    save_and_display_matrix(matrix, output_image_path)
    #======================== End of convertion ============================="""
