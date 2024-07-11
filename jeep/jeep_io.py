from config.constants import XY_SPEED, STEP_SIZE_X, STEP_SIZE_Y
from robomaster import robot

OPPOSITE_DIRECTION = {'Up': 'Down', 'Down': 'Up', 'Right': 'Left', 'Left': 'Right'}


def move_chassis(chassis, direction, step_size=None):
    step_size_x = step_size if step_size else STEP_SIZE_X
    step_size_y = step_size if step_size else STEP_SIZE_Y
    if direction == "Up":
        chassis.move(x=step_size_x, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
    if direction == "Down":
        chassis.move(x=-step_size_x, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
    if direction == "Left":
        chassis.move(x=0, y=-step_size_y, z=0, xy_speed=XY_SPEED).wait_for_completed()
    if direction == "Right":
        chassis.move(x=0, y=step_size_y, z=0, xy_speed=XY_SPEED).wait_for_completed()
    chassis.stop()


def correct_last_move_drift(chassis, last_move_direction):
    move_chassis(chassis=chassis,
                 direction=OPPOSITE_DIRECTION.get(last_move_direction),
                 step_size=0.1)


def send_directions_to_jeep(directions):
    # Initialize the RoboMaster robot with the specified connection type and other relevant details
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type='sta', proto_type='tcp')
    chassis = ep_robot.chassis
    # Move 2 Meters
    chassis.move(x=-1.2, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
    chassis.stop()
    last_move = None
    for direction in directions:
        last_move = direction
        move_chassis(chassis, direction)
    correct_last_move_drift(chassis, last_move)
    ep_robot.close()
