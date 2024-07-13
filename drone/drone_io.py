from time import sleep
from typing import Any, Dict

import numpy as np
import requests
from PIL import Image


class DroneController:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
        self.server_addr = f"http://{self.ip}:{self.port}"
        r = requests.get(url=self.server_addr)
        assert r.content == b"Connected"
        self.enable()
        self.startcamerastream()

    def makeReqAndReturnJSON(self, route: str) -> Dict[str, Any]:
        r = requests.get(url=f"{self.server_addr}{route}")
        return r.json()

    def enable(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/Enable')

    def disable(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/Disable')

    def takeOff(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON(f'/TakeOff')

    def land(self) -> Dict[str, Any]:
        for i in range(10):
            self.makeReqAndReturnJSON('/Land')
            sleep(1)
        return self.makeReqAndReturnJSON('/Land')

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

    def movesideways(self, param, time) -> Dict[str, Any]:
        time = round(1000 * time)
        return self.makeReqAndReturnJSON(f'/MoveSideways/{param}/{time}')

    def startcamerastream(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/StartCameraStream')

    def camerastream(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/CameraStream')

    def stopcamerastream(self) -> Dict[str, Any]:
        return self.makeReqAndReturnJSON('/StopCameraStream')

    def capture_and_save_rgba_image(self, save_to_path) -> Dict[str, Any]:
        camera_stream = self.camerastream()
        image = camera_stream["state"]
        print("Image Captured")
        for i in range(len(image)):
            if image[i] < 0:
                image[i] += 256
        print("Fixed Image Values")
        camera_stream['image'] = image
        self.save_rgba_image_from_int_list(image, camera_stream['width'], camera_stream['height'], save_to_path)
        return camera_stream

    @staticmethod
    def save_rgba_image_from_int_list(int_list, width, height, output_filename):
        if len(int_list) != width * height * 4:
            raise ValueError("The length of the int_list does not match the expected dimensions of the image.")
        rgba_array = np.array(int_list, dtype=np.uint8).reshape((height, width, 4))
        image = Image.fromarray(rgba_array, 'RGBA')
        image.save(output_filename)
