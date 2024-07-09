import numpy as np
import heapq


def compress_map(map, k):
    n, m = map.shape
    compressed_n, compressed_m = n // k, m // k
    compressed_map = np.zeros((compressed_n, compressed_m), dtype=int)
    for i in range(compressed_n):
        for j in range(compressed_m):
            subarray = map[i * k:(i + 1) * k, j * k:(j + 1) * k]
            compressed_map[i, j] = subarray.max()
    return compressed_map


def compress_map_by_ratio(curr_map, ratio1, ratio2):  # jeep size divided by map length = ratio
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
    compressed_map, step_size = compress_map_by_ratio(birds_eye_img, 35 / 120, 35 / 180)
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
            return
    else:
        print("No destinations found.")
    return


'''
# Example usage
original_map = np.array([
    [0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0],
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


def generate_map(height, width, obstacle_probability=0.01):
    # Create an array filled with 0s
    map_array = np.zeros((height, width), dtype=int)

    # Randomly place obstacles (1s) with the given probability
    obstacle_mask = np.random.rand(height, width) < obstacle_probability
    map_array[obstacle_mask] = 1

    # Randomly place a single destination (2)
    while True:
        dest_x = np.random.randint(0, height)
        dest_y = np.random.randint(0, width)
        if map_array[dest_x, dest_y] == 0:  # Ensure it doesn't overwrite an obstacle
            map_array[dest_x, dest_y] = 2
            break

    return map_array

# Generate the map
# height = 2000
# width = 3000
# map_array = generate_map(height, width)
# map_array[0]=2
# # Print a small portion of the map to verify
# print(map_array[:10, :10])

# print(plan_path(map_array,(0,0),2))
