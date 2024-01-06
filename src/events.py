# pylint: disable=maybe-no-member
from guiElements.window import WindowEvent
from pygame.key import get_pressed
from pygame import K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_LCTRL, K_LSHIFT, K_RCTRL, K_RSHIFT, K_SPACE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_ESCAPE


class GameEvents(WindowEvent):
    def __init__(self):
        super().__init__()

        self.keys = {
            "a": K_a,
            "b": K_b,
            "c": K_c,
            "d": K_d,
            "e": K_e,
            "f": K_f,
            "g": K_g,
            "h": K_h,
            "i": K_i,
            "j": K_j,
            "k": K_k,
            "l": K_l,
            "m": K_m,
            "n": K_n,
            "o": K_o,
            "p": K_p,
            "q": K_q,
            "r": K_r,
            "s": K_s,
            "t": K_t,
            "u": K_u,
            "v": K_v,
            "w": K_w,
            "x": K_x,
            "y": K_y,
            "z": K_z,
            "0": K_0,
            "1": K_1,
            "2": K_2,
            "3": K_3,
            "4": K_4,
            "5": K_5,
            "6": K_6,
            "7": K_7,
            "8": K_8,
            "9": K_9,
            "space": K_SPACE,
            "lctrl": K_LCTRL,
            "rctrl": K_RCTRL,
            "lshift": K_LSHIFT,
            "rshift": K_RSHIFT
        }


    def eventsCheck(self):
        super().eventsCheck()

        self.events["keysDown"] = self.getKeysDown()



    def getKeysDown(self):
        """Gets all the keys that are being pressed

        Returns:
            Sequence[bool]: the set of keys that are being pressed at the moment
        """
        return get_pressed()


    def keyIsPressed(self, key:str) -> bool:
        """Check if a specific key is being pressed

        Args:
            key (str): the key to be checked

        Raises:
            KeyError: If the key is not in the dict of preset keys
            or if the eventsCheck method hasn't been called first

        Returns:
            bool: True if its being pressed, False otherwise
        """
        return self.events["keysDown"][self.keys[key]]
