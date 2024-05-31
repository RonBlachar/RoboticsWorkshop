from drone_io import get_drone_img
from jeep_io import send_instructions_to_jeep
from birds_eye import apply_birds_eye
from preprocess import get_boundaries, get_destination, get_obstacles
from path_planner import plan_path

if __name__ == "__main__":
    drone_img = get_drone_img()
    boundaries = get_boundaries(drone_img)
    birds_eye_img = apply_birds_eye(drone_img, *boundaries)
    obstacles = get_obstacles(birds_eye_img)
    destination = get_destination(birds_eye_img)
    path = plan_path(birds_eye_img, obstacles, destination)
    send_instructions_to_jeep(path)
