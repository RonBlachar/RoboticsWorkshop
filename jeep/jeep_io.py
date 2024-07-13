from config.constants import XY_SPEED, STEP_SIZE_X, STEP_SIZE_Y
from robomaster import robot


class JeepController:
    OPPOSITE_DIRECTION = {'Up': 'Down', 'Down': 'Up', 'Right': 'Left', 'Left': 'Right'}

    def __init__(self):
        self.ep_robot = robot.Robot()
        self.ep_robot.initialize(conn_type='sta', proto_type='tcp')
        self.chassis = self.ep_robot.chassis

    def move_chassis(self, direction, step_size=None):
        """
        Moves jeep in the given direction (Up, Down, Right, Left) with the given step size.
        :param direction:
        :param step_size: float.
        step size in meters. for example: step_size=0.1 moves the jeep 10 cm in the given direction.
        :return:
        """
        step_size_x = step_size if step_size else STEP_SIZE_X
        step_size_y = step_size if step_size else STEP_SIZE_Y
        if direction == "Up":
            self.chassis.move(x=step_size_x, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
        if direction == "Down":
            self.chassis.move(x=-step_size_x, y=0, z=0, xy_speed=XY_SPEED).wait_for_completed()
        if direction == "Left":
            self.chassis.move(x=0, y=-step_size_y, z=0, xy_speed=XY_SPEED).wait_for_completed()
        if direction == "Right":
            self.chassis.move(x=0, y=step_size_y, z=0, xy_speed=XY_SPEED).wait_for_completed()
        self.chassis.stop()

    def _correct_last_move_drift(self, last_move_direction):
        self.move_chassis(direction=self.OPPOSITE_DIRECTION.get(last_move_direction),
                          step_size=0.1)

    def move_jeep_by_directions(self, directions, start_move_x=0, start_move_y=0):
        if start_move_x or start_move_y:
            self.chassis.move(x=start_move_x, y=start_move_y, z=0, xy_speed=XY_SPEED).wait_for_completed()
            self.chassis.stop()
        last_move = None
        for direction in directions:
            last_move = direction
            self.move_chassis(direction)
        self._correct_last_move_drift(last_move)
        self.ep_robot.close()
