import numpy as np
import heapq
from itertools import permutations


def compress_map(original_map, k):
    n = original_map.shape[0]
    compressed_size = n // k
    compressed_map = np.zeros((compressed_size, compressed_size), dtype=int)

    for i in range(compressed_size):
        for j in range(compressed_size):
            subarray = original_map[i * k:(i + 1) * k, j * k:(j + 1) * k]
            if 2 in subarray:
                compressed_map[i, j] = 2
            elif 1 in subarray:
                compressed_map[i, j] = 1
            else:
                compressed_map[i, j] = 0

    return compressed_map


def is_valid_move(map_array, x, y, jeep_height, jeep_width):
    rows, cols = map_array.shape
    if x < 0 or y < 0 or x + jeep_height > rows or y + jeep_width > cols:
        return False
    for i in range(jeep_height):
        for j in range(jeep_width):
            if map_array[x + i, y + j] == 1:
                return False
    return True


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


def a_star(map_array, start, goal, jeep_height, jeep_width):
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
                if is_valid_move(map_array, neighbor[0], neighbor[1], jeep_height, jeep_width):
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def plan_path(birds_eye_img, start, destinations, jeep_height, jeep_width):
    min_tour = None
    min_tour_length = float('inf')

    for perm in permutations(destinations):
        tour_length = 0
        current_start = start
        current_tour = []

        for destination in perm:
            path = a_star(birds_eye_img, current_start, destination, jeep_height, jeep_width)
            if path is None:
                break
            tour_length += len(path) - 1
            current_tour.extend(path[:-1])
            current_start = destination

        path_back = a_star(birds_eye_img, current_start, start, jeep_height, jeep_width)
        if path_back is None:
            continue

        tour_length += len(path_back) - 1
        current_tour.extend(path_back)

        if tour_length < min_tour_length:
            min_tour_length = tour_length
            min_tour = current_tour

    return min_tour


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


'''
Example usage

original_map = np.array([
    [0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
k = 2

compressed_map = compress_map(original_map, k)
print("Compressed Map:")
print(compressed_map)

start = (0, 0)  # Updated start position to ensure the jeep can start without overlapping obstacles
jeep_height = 1
jeep_width = 1

destinations = find_destinations(compressed_map)
print("Destinations:", destinations)

tour = plan_path(compressed_map, start, destinations, jeep_height, jeep_width)
directions = path_to_directions(tour)
print("Tour:", tour)
print("Directions:", directions)
 '''