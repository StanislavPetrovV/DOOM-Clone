from settings import *
from enum import IntEnum, auto
from pyray import is_key_down, is_key_pressed, KeyboardKey


class Key(IntEnum):
    #
    FORWARD = KeyboardKey.KEY_W
    BACK = KeyboardKey.KEY_S
    STRAFE_LEFT = KeyboardKey.KEY_A
    STRAFE_RIGHT = KeyboardKey.KEY_D
    UP = KeyboardKey.KEY_Q
    DOWN = KeyboardKey.KEY_E
    MAP = KeyboardKey.KEY_M
    SCREEN_SHOT = KeyboardKey.KEY_O


class InputHandler:
    def __init__(self, engine):
        self.engine = engine
        self.camera = engine.camera

    def update(self):
        # ----------- camera control ----------- #
        if is_key_down(Key.FORWARD):
            self.camera.step_forward()
        #
        elif is_key_down(Key.BACK):
            self.camera.step_back()

        if is_key_down(Key.STRAFE_RIGHT):
            self.camera.step_right()
        #
        elif is_key_down(Key.STRAFE_LEFT):
            self.camera.step_left()

        if is_key_down(Key.UP):
            self.camera.step_up()
        #
        elif is_key_down(Key.DOWN):
            self.camera.step_down()
        # -------------------------------------- #

        if is_key_pressed(Key.MAP):
            self.engine.map_renderer.should_draw = not self.engine.map_renderer.should_draw
            self.engine.view_renderer.update_screen_tint()

        if is_key_pressed(Key.SCREEN_SHOT):
            ray.take_screenshot('screen_shot.png')