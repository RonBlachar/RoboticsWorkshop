from asyncio import sleep

from drone.drone_io import DJIControlClient
from jeep.jeep_io import send_directions_to_jeep
from path_planner.path_planner import create_path

if __name__ == "__main__":
    drone = DJIControlClient("172.20.10.6", 8080)
    drone.enable()
    drone.startcamerastream()
    drone.takeOff()
    drone.rotatecamera(90)
    sleep(3)
    drone.moveup(40, 3.5)
    sleep(2)
    pic = drone.photo()
    sleep(1)
    drone.land()
    drone.disable()
    path = create_path('photo.png')
    print(path)
    sleep(2)
    send_directions_to_jeep(path)
