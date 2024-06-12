import os
import matplotlib.pyplot as plt
import cv2
from config.constants import BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, BOUNDARIES_UPPER_BOUND2, OBSTACLES_LOWER_BOUND1, OBSTACLES_UPPER_BOUND1, OBSTACLES_LOWER_BOUND2, OBSTACLES_UPPER_BOUND2, DESTINATION_LOWER_BOUND1, DESTINATION_UPPER_BOUND1, DESTINATION_LOWER_BOUND2, DESTINATION_UPPER_BOUND2, JEEP_SIZE
from image_processing.birds_eye import apply_birds_eye, plot_birds_eye_view
from image_processing.preprocess import find_boundaries, convert_birds_eye_to_matrix, order_boundaries, plot_img_with_boundaries
from path_planner.path_planner import plan_path


def create_path(img_path):
    print("**************** Start of the process *********************")
    image = cv2.imread(img_path)
    boundaries = find_boundaries(image, BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, BOUNDARIES_UPPER_BOUND2)
    plot_img_with_boundaries(image, boundaries)#Plot the original image with the detected boundaries 
    ord_boundaries = order_boundaries(boundaries)
    birds_eye_img = apply_birds_eye(image, ord_boundaries)
    plot_birds_eye_view(birds_eye_img) #Plot the birds eye image
    categorized_img_matrix = convert_birds_eye_to_matrix(birds_eye_img)
    direction_array = plan_path(categorized_img_matrix, start=(0, 0), jeep_size=JEEP_SIZE)
    return direction_array


if __name__ == "__main__":
    print(create_path("images/WhatsApp Image 2024-06-11 at 14.29.05.jpeg"))
    print("************** End of the process ***************")