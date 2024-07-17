import heapq

import cv2
import numpy as np

from config.constants import BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, \
    BOUNDARIES_UPPER_BOUND2, NAVIGATION_AREA_HEIGHT, JEEP_SIZE, NAVIGATION_AREA_WIDTH
from image_processing.birds_eye import apply_birds_eye, plot_birds_eye_view, plot_path_on_birds_eye_image
from image_processing.postprocess import plot_heatmap_over_image
from image_processing.preprocess import find_boundaries, plot_img_with_boundaries, order_boundaries, \
    convert_birds_eye_image_to_matrix


def compress_map_by_ratio(curr_map, ratio1, ratio2):
    n, m = curr_map.shape
    compressed_n, compressed_m = int(1 // ratio1) + 1, int(1 // ratio2) + 1
    compressed_map = np.zeros((compressed_n, compressed_m), dtype=int)
    k = int(0.9 * n * ratio1)
    for i in range(compressed_n):
        for j in range(compressed_m):
            subarray = curr_map[i * k:(i + 1) * k, j * k:(j + 1) * k]
            compressed_map[i, j] = subarray.max()
    return compressed_map, k


def find_destinations(map_array):
    destinations = []
    rows, cols = map_array.shape
    for i in range(rows):
        for j in range(cols):
            if map_array[i, j] == 2:
                destinations.append((i, j))
    return destinations


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(map_array, start, goal):
    rows, cols = map_array.shape
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if map_array[neighbor[0], neighbor[1]] != 1:
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None


def path_to_directions(path):
    directions = []
    for i in range(1, len(path)):
        dx = path[i][0] - path[i - 1][0]
        dy = path[i][1] - path[i - 1][1]
        if dx == 1:
            directions.append('Down')
        elif dx == -1:
            directions.append('Up')
        elif dy == 1:
            directions.append('Right')
        elif dy == -1:
            directions.append('Left')
    return directions


def plan_path(birds_eye_img, start):
    compressed_map, step_size = compress_map_by_ratio(birds_eye_img, JEEP_SIZE / NAVIGATION_AREA_HEIGHT,
                                                      JEEP_SIZE / NAVIGATION_AREA_WIDTH)
    print(compressed_map)
    destinations = find_destinations(compressed_map)
    # Assuming we only have one destination in the map for simplicity.
    if destinations:
        goal = destinations[0]
        path = a_star(compressed_map, start, goal)
        if path:
            directions = path_to_directions(path)
            return directions, step_size
        else:
            print("No path found.")
    else:
        print("No destinations found.")
    return None


def create_navigation_directions(img_path):
    image = cv2.imread(img_path)
    boundaries = find_boundaries(image, BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2,
                                 BOUNDARIES_UPPER_BOUND2)
    plot_img_with_boundaries(image, boundaries)  # Plot the original image with the detected boundaries
    ord_boundaries = order_boundaries(boundaries)
    birds_eye_img = apply_birds_eye(image, ord_boundaries)
    plot_birds_eye_view(birds_eye_img)  # Plot the birds eye image
    categorized_img_matrix = convert_birds_eye_image_to_matrix(birds_eye_img)
    plot_heatmap_over_image(birds_eye_img, categorized_img_matrix)
    direction_array, step_size = plan_path(categorized_img_matrix, start=(0, 0))
    plot_path_on_birds_eye_image(birds_eye_img, direction_array, step_size=step_size)
    return direction_array
