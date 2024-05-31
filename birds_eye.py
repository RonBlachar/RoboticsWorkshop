from typing import Tuple, List

import cv2
import numpy as np


def apply_birds_eye(drone_img: np.array, pt_a: Tuple[int, int], pt_b: Tuple[int, int], pt_c: Tuple[int, int],
                    pt_d: Tuple[int, int]) -> List[Tuple[int, int]]:
    # L2 norm
    width_ad = np.sqrt(((pt_a[0] - pt_d[0]) ** 2) + ((pt_a[1] - pt_d[1]) ** 2))
    width_bc = np.sqrt(((pt_b[0] - pt_c[0]) ** 2) + ((pt_b[1] - pt_c[1]) ** 2))
    max_width = max(int(width_ad), int(width_bc))
    height_ab = np.sqrt(((pt_a[0] - pt_b[0]) ** 2) + ((pt_a[1] - pt_b[1]) ** 2))
    height_cd = np.sqrt(((pt_c[0] - pt_d[0]) ** 2) + ((pt_c[1] - pt_d[1]) ** 2))
    max_height = max(int(height_ab), int(height_cd))

    input_pts = np.float32([pt_a, pt_b, pt_c, pt_d])
    output_pts = np.float32([[0, 0],
                             [0, max_height - 1],
                             [max_width - 1, max_height - 1],
                             [max_width - 1, 0]])
    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(input_pts, output_pts)
    out = cv2.warpPerspective(drone_img, M, (max_width, max_height), flags=cv2.INTER_LINEAR)
    return out
