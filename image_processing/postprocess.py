import cv2
import numpy as np

from image_processing.plot_utils import plot_image


def plot_heatmap_over_image(image, heatmap_matrix, alpha=1):
    """
    Plots a heatmap over the original HSV image.

    Parameters:
    - image: numpy array, the original image in HSV format.
    - heatmap_matrix: 2D numpy array, matrix of 0/1/2 values representing the heat map.
    - alpha: float, transparency factor for the overlay (default is 0.5).
    """
    # Create a color map for the heat map matrix
    colormap = np.zeros((heatmap_matrix.shape[0], heatmap_matrix.shape[1], 3), dtype=np.uint8)
    colormap[heatmap_matrix == 0] = [0, 0, 255]  # Blue for 0
    colormap[heatmap_matrix == 1] = [0, 255, 0]  # Green for 1
    colormap[heatmap_matrix == 2] = [255, 0, 0]  # Red for 2
    # Combine the heat map with the original image using transparency
    overlay = cv2.addWeighted(image, 1 - alpha, colormap, alpha, 0)
    plot_image(overlay, 'Image with Heat Map Overlay')
