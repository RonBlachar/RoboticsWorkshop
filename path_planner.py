import numpy as np
import heapq
from itertools import permutations


def compress_map(map, k):
    n, m = map.shape
    compressed_n, compressed_m = n // k, m // k
    compressed_map = np.zeros((compressed_n, compressed_m), dtype=int)

    for i in range(compressed_n):
        for j in range(compressed_m):
            subarray = map[i * k:(i + 1) * k, j * k:(j + 1) * k]
            if 2 in subarray:
                compressed_map[i, j] = 2
            elif 1 in subarray:
                compressed_map[i, j] = 1
            else:
                compressed_map[i, j] = 0

    return compressed_map


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


def plan_path(birds_eye_img, start, jeep_size):
    compressed_map = compress_map(birds_eye_img, jeep_size)
    destinations = find_destinations(compressed_map)
    # Assuming we only have one destination in the map for simplicity.
    if destinations:
        goal = destinations[0]
        path = a_star(compressed_map, start, goal)
        if path:
            directions = path_to_directions(path)
            return directions
        else:
            print("No path found.")
            return
    else:
        print("No destinations found.")
    return

'''
# Example usage
original_map = np.array([
    [0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
k = 2
comp_map = compress_map(original_map, k)
print("Compressed Map:")
print(comp_map)

start = (0, 0)  # Starting position
destinations = find_destinations(comp_map)
print("Destinations:", destinations)

# Assuming we only have one destination in the map for simplicity.
print(plan_path(original_map, start, 2))
'''