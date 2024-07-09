from config.constants import XY_SPEED, STEP_SIZE_X, STEP_SIZE_Y
from robomaster import robot

OPPOSITE_DIRECTION = {'Up': 'Down', 'Down': 'Up', 'Right': 'Left', 'Left': 'Right'}


def wrapper(directions):
    # Initialize the RoboMaster robot with the specified connection type and other relevant details
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type='sta', proto_type='tcp')
    # Create a chassis object
    chassis = ep_robot.chassis
    chassis.move(x=-1.2, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
    chassis.stop()
    last_move = None
    for direction in directions:
        last_move = direction
        if direction == "Up":
            chassis.move(x=STEP_SIZE_X, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
            chassis.stop()
            continue
        if direction == "Down":
            chassis.move(x=-STEP_SIZE_X, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
            chassis.stop()
            continue
        if direction == "Left":
            chassis.move(x=0, y=-STEP_SIZE_Y, z=0, xy_speed=XY_SPEED).wait_for_completed()
            chassis.stop()
            continue
        if direction == "Right":
            chassis.move(x=0, y=STEP_SIZE_Y, z=0, xy_speed=XY_SPEED).wait_for_completed()
            chassis.stop()
            continue
    if last_move in ['Up', 'Down']:
        chassis.move(x=0.1 if last_move == 'Down' else -0.1, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
        chassis.stop()
    if last_move in ['Right', 'Left']:
        chassis.move(x=0, y=0.1 if last_move == 'Right' else -0.1, z=0, xy_speed=XY_SPEED).wait_for_completed()
        chassis.stop()
    # Close the connection
    ep_robot.close()
