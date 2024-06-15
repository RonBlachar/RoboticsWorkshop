import numpy as np
#To remember - the color ranges are according to hsv (not rgb)
#For example - for something that is blue at the original image, we will use the blue hsv range 
#Red color!
BOUNDARIES_LOWER_BOUND1 = np.array([0, 150, 150])
BOUNDARIES_UPPER_BOUND1 = np.array([10, 255, 255])
BOUNDARIES_LOWER_BOUND2 = np.array([170, 100, 100])
BOUNDARIES_UPPER_BOUND2 = np.array([180, 255, 255])

#Black color!
OBSTACLES_LOWER_BOUND1 = np.array([0, 0, 0])
OBSTACLES_UPPER_BOUND1 = np.array([180, 255, 30])
OBSTACLES_LOWER_BOUND2 = np.array([0, 0, 0])
OBSTACLES_UPPER_BOUND2 = np.array([180, 255, 50])

#Blue color!
DESTINATION_LOWER_BOUND1 = np.array([90, 50, 50])
DESTINATION_UPPER_BOUND1 = np.array([130, 255, 255])
DESTINATION_LOWER_BOUND2 = np.array([100, 100, 100])
DESTINATION_UPPER_BOUND2 = np.array([140, 255, 255])

JEEP_SIZE = 100
