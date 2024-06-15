import os
import matplotlib.pyplot as plt
import cv2
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from config.constants import BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, BOUNDARIES_UPPER_BOUND2, JEEP_SIZE
from image_processing.birds_eye import apply_birds_eye
from image_processing.preprocess import find_boundaries, process_image, order_boundaries
from path_planner.path_planner import plan_path
app = FastAPI()


@app.get("/")
def hello():
    return {"API": "API is working fine"}


@app.post("/upload_image")
async def upload_image(img_file: UploadFile = File(...)):
    if '.jpg' in img_file.filename or '.jpeg' in img_file.filename or '.png' in img_file.filename:
        file_save_path = "./images/" + img_file.filename
        if not os.path.exists("./images"):
            os.makedirs("./images")

        with open(file_save_path, "wb") as f:
            f.write(img_file.file.read())

        # return {"a": file_save_path}
        direction_array = create_path(file_save_path)


def create_path(img_path):
    print("*************")
    image = cv2.imread(img_path)
    boundaries = find_boundaries(image, BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, BOUNDARIES_UPPER_BOUND2)
    boundaries = order_boundaries(boundaries)
    birds_eye_img = apply_birds_eye(image, *boundaries)
    plt.imshow(birds_eye_img)
    plt.show()
    categorized_img_matrix = process_image(birds_eye_img)
    direction_array = plan_path(categorized_img_matrix, start=(0, 0), jeep_size=JEEP_SIZE)
    return direction_array


if __name__ == "__main__":
    # uvicorn.run(app)
    print(create_path('images/input3.jpeg'))
