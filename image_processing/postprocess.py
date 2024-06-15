import cv2
import numpy as np
from matplotlib import pyplot as plt


def overlay_heat_map(image, heat_map_matrix, alpha=0.5):
    """
    Overlays a heat map on the original HSV image.

    Parameters:
    - hsv_image: numpy array, the original image in HSV format.
    - heat_map_matrix: 2D numpy array, matrix of 0/1/2 values representing the heat map.
    - alpha: float, transparency factor for the overlay (default is 0.5).

    Returns:
    - None, displays the image with heat map overlay.
    """
    # Create a color map for the heat map matrix
    colormap = np.zeros((heat_map_matrix.shape[0], heat_map_matrix.shape[1], 3), dtype=np.uint8)
    colormap[heat_map_matrix == 0] = [0, 0, 255]  # Blue for 0
    colormap[heat_map_matrix == 1] = [0, 255, 0]  # Green for 1
    colormap[heat_map_matrix == 2] = [255, 192, 203]  # Red for 2
    # Combine the heat map with the original image using transparency
    overlay = cv2.addWeighted(image, 1 - alpha, colormap, alpha, 0)

    # Display the image with the heat map
    plt.figure(figsize=(10, 10))
    plt.imshow(overlay)
    plt.title('Image with Heat Map Overlay')
    plt.axis('off')
    plt.show()
