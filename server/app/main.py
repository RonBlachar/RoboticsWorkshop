import os
import matplotlib.pyplot as plt
import cv2
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pickle
from pathlib import Path

from config.constants import BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, BOUNDARIES_UPPER_BOUND2, OBSTACLES_LOWER_BOUND1, OBSTACLES_UPPER_BOUND1, OBSTACLES_LOWER_BOUND2, OBSTACLES_UPPER_BOUND2, DESTINATION_LOWER_BOUND1, DESTINATION_UPPER_BOUND1, DESTINATION_LOWER_BOUND2, DESTINATION_UPPER_BOUND2, JEEP_SIZE
from image_processing.birds_eye import apply_birds_eye, plot_birds_eye_view, plot_path_on_birds_eye_image
from image_processing.preprocess import find_boundaries, convert_birds_eye_to_matrix, order_boundaries, plot_img_with_boundaries
from config.constants import BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2, \
    BOUNDARIES_UPPER_BOUND2, OBSTACLES_LOWER_BOUND1, OBSTACLES_UPPER_BOUND1, OBSTACLES_LOWER_BOUND2, \
    OBSTACLES_UPPER_BOUND2, DESTINATION_LOWER_BOUND1, DESTINATION_UPPER_BOUND1, DESTINATION_LOWER_BOUND2, \
    DESTINATION_UPPER_BOUND2, JEEP_SIZE
from image_processing.birds_eye import apply_birds_eye, plot_birds_eye_view
from image_processing.preprocess import find_boundaries, convert_birds_eye_to_matrix, order_boundaries, \
    plot_img_with_boundaries
from path_planner.path_planner import plan_path

app = FastAPI()


@app.get("/")
def hello():
    return {"API": "API is working fine"}


@app.post("/upload_image")
async def upload_image(img_file: UploadFile = File(...)):
    if '.jpg' in img_file.filename or '.jpeg' in img_file.filename or '.png' in img_file.filename:
        file_save_path = f"./drone_images/{img_file.filename}"
        if not os.path.exists("./drone_images"):
            os.makedirs("./drone_images")
        print(file_save_path)
        with open(file_save_path, "wb") as f:
            f.write(img_file.file.read())

        direction_array = create_path(file_save_path)
        img_name = Path(img_file.filename).stem
        result_file = f"./results/{img_name}"
        if not os.path.exists("./results"):
            os.makedirs("./results")
        with open(result_file, 'wb') as f:
            pickle.dump(direction_array, f)


@app.get("/get_image_directions/")
async def get_image_directions(img_name: str):
    with open(f"results/{img_name}", "rb") as fp:
        res = pickle.load(fp)
    return res


def create_path(img_path):
    print("**************** Start of the process *********************")
    image = cv2.imread(img_path)
    boundaries = find_boundaries(image, BOUNDARIES_LOWER_BOUND1, BOUNDARIES_UPPER_BOUND1, BOUNDARIES_LOWER_BOUND2,
                                 BOUNDARIES_UPPER_BOUND2)
    plot_img_with_boundaries(image, boundaries)  # Plot the original image with the detected boundaries
    ord_boundaries = order_boundaries(boundaries)
    birds_eye_img = apply_birds_eye(image, ord_boundaries)
    plot_birds_eye_view(birds_eye_img)  # Plot the birds eye image
    categorized_img_matrix = convert_birds_eye_to_matrix(birds_eye_img)
    direction_array = plan_path(categorized_img_matrix, start=(0, 0), jeep_size=JEEP_SIZE)
    plot_path_on_birds_eye_image(birds_eye_img, direction_array)
    return direction_array


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # path = create_path("/Users/ronblachar/PycharmProjects/RoboticsWorkshop/images/WhatsApp Image 2024-06-11 at 14.29.05.jpeg")
    # print("************** End of the process ***************")
