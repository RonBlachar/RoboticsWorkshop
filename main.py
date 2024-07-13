from asyncio import sleep

from drone.drone_io import DroneController
from jeep.jeep_io import JeepController
from path_planner.path_planner import create_navigation_directions


def drone_main():
    drone = DroneController("172.20.10.6", 8080)
    drone.takeOff()
    drone.rotatecamera(90)
    sleep(3)
    drone.moveup(40, 3.5)
    sleep(2)
    drone.capture_and_save_rgba_image(save_to_path='drone_image.png')
    sleep(1)
    drone.land()
    drone.disable()


if __name__ == "__main__":
    drone_main()
    navigation_directions = create_navigation_directions('drone_image.png')
    print(navigation_directions)
    sleep(2)
    jeep = JeepController()
    jeep.move_jeep_by_directions(navigation_directions,
                                 start_move_x=-1.2)  # Initially moves jeep 1.2 meters to enter the navigation area
