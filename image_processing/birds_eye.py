from typing import Tuple, List
import matplotlib.pyplot as plt
import cv2
import numpy as np


# def apply_birds_eye(drone_img: np.array, pt_a: Tuple[int, int], pt_b: Tuple[int, int], pt_c: Tuple[int, int],
#                     pt_d: Tuple[int, int]) -> List[Tuple[int, int]]:
#     # L2 norm
#     width_ad = np.sqrt(((pt_a[0] - pt_d[0]) ** 2) + ((pt_a[1] - pt_d[1]) ** 2))
#     width_bc = np.sqrt(((pt_b[0] - pt_c[0]) ** 2) + ((pt_b[1] - pt_c[1]) ** 2))
#     max_width = max(int(width_ad), int(width_bc))
#     height_ab = np.sqrt(((pt_a[0] - pt_b[0]) ** 2) + ((pt_a[1] - pt_b[1]) ** 2))
#     height_cd = np.sqrt(((pt_c[0] - pt_d[0]) ** 2) + ((pt_c[1] - pt_d[1]) ** 2))
#     max_height = max(int(height_ab), int(height_cd))

#     input_pts = np.float32([pt_a, pt_b, pt_c, pt_d])
#     output_pts = np.float32([[0, 0],
#                              [0, max_height - 1],
#                              [max_width - 1, max_height - 1],
#                              [max_width - 1, 0]])
#     # Compute the perspective transform M
#     M = cv2.getPerspectiveTransform(input_pts, output_pts)
#     out = cv2.warpPerspective(drone_img, M, (max_width, max_height), flags=cv2.INTER_LINEAR)
#     return out

def apply_birds_eye(drone_img: np.array, coordinates):
    # L2 norm
    tl = coordinates[0]
    tr = coordinates[1]
    br = coordinates[2]
    bl = coordinates[3]
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    distance = np.array([
        [0,0],
        [max_width -1, 0],
        [max_width -1, max_height -1],
        [0, max_width -1]], dtype = "float32")
    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(coordinates, distance)
    wraped = cv2.warpPerspective(drone_img, M, (max_width, max_height),)
    # Crop the image to exclude boundary regions
    margin = 5  # Margin to exclude boundary regions (adjust as needed)
    cropped = wraped[margin:max_height-margin, margin:max_width-margin]

    return cropped

def plot_birds_eye_view(birds_eye_img):
    plt.imshow(birds_eye_img)
    plt.title("Bird's-Eye View")
    plt.axis('off')
    plt.show()

def plot_path_on_birds_eye_image(birds_eye_img, direction_array):
    image_rgb = cv2.cvtColor(birds_eye_img, cv2.COLOR_BGR2RGB)
    # Define the starting point
    x, y = 0, 0

    # Define the step size (assuming each step corresponds to the size of a tile)
    step_size = 60  # Adjust this value based on the image scale

    # List to store the coordinates of the path
    path_coordinates = [(x * step_size, y * step_size)]

    # Calculate the coordinates for the given orders
    for order in direction_array:
        if order == 'Right':
            y += 1
        elif order == 'Down':
            x += 1
        elif order == 'Left':
            y -= 1
        elif order == 'Up':
            x -= 1
        path_coordinates.append((y * step_size, x * step_size))

    # Draw the path on the image
    for coord in path_coordinates:
        cv2.circle(image_rgb, coord, radius=5, color=(0, 255, 0), thickness=-1)

    # Display the image with the path
    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.title('Path Visualization')
    plt.axis('off')
    plt.show()