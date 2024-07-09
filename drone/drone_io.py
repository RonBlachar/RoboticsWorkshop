from typing import Any, Dict
import requests
from time import sleep
import cv2
import numpy as np
from PIL import Image

from jeep.jeep_io import wrapper
from server.app.main import create_path


class DJIControlClient:

    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

        self.server_addr = f"http://{self.ip}:{self.port}"

        r = requests.get(url=self.server_addr)

        assert r.content == b"Connected"

    def makeReqAndReturnJSON(self, route: str) -> Dict[str, Any]:
        r = requests.get(url=f"{self.server_addr}{route}")
        return r.json()

    def takeOff(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/TakeOff')

    def camerastream(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/CameraStream')

    def startcamerastream(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/StartCameraStream')

    def stopcamerastream(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/StopCameraStream')

    def land(self) -> Dict[str, Any]:
        for i in range(10):
            self.makeReqAndReturnJSON('/Land')
            sleep(1)
        return self.makeReqAndReturnJSON('/Land')

    def enable(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/Enable')

    def disable(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/Disable')

    def cameradown(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/CameraDown')

    def cameraup(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/CameraUp')

    def moveup(self, param, time) -> Dict[str, Any]:
        time = round(1000 * time)
        return self.makeReqAndReturnJSON(f'/MoveUp/{param}/{time}')

    def rotatecamera(self, angle) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/RotateCamera/{angle}')

    def moveforward(self, forward, right, time) -> Dict[str, Any]:
        time = round(1000 * time)
        return self.makeReqAndReturnJSON(f'/MoveForward/{forward}/{right}/{time}')
        """forward = -forward//2
        right = -right//2
        time = 100
        return self.makeReqAndReturnJSON(f'/MoveForward/{forward}/{right}/{time}')"""

    def rotate(self, param, time) -> Dict[str, Any]:
        time = round(1000 * time)
        return self.makeReqAndReturnJSON(f'/Rotate/{param}/{time}')

    def takepicture(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/TakePicture')

    def initialize(self) -> Dict[str, Any]:
        self.enable()
        self.startcamerastream()
        self.camerastream()
        return self.cameradown()

    def movesideways(self, param, time) -> Dict[str, Any]:
        time = round(1000 * time)
        return self.makeReqAndReturnJSON(f'/MoveSideways/{param}/{time}')

    def photo(self) -> Dict[str, Any]:
        pic = self.camerastream()
        photo = pic["state"]
        print(1)
        for i in range(len(photo)):
            if photo[i] < 0:
                photo[i] += 256
        print(2)
        pic['photo'] = photo
        self.int_list_to_rgba_image(photo, pic['width'], pic['height'], 'photo.png')
        return pic

    @staticmethod
    def int_list_to_rgba_image(int_list, width, height, output_filename):
        # Ensure the list length matches the expected size
        if len(int_list) != width * height * 4:
            raise ValueError("The length of the int_list does not match the expected dimensions of the image.")

        # Convert the list to a NumPy array and reshape it
        rgba_array = np.array(int_list, dtype=np.uint8).reshape((height, width, 4))

        # Create an image from the array
        image = Image.fromarray(rgba_array, 'RGBA')

        # Save the image
        image.save(output_filename)


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
wrapper(path)

