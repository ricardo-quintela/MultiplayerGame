from guiElements.window import Window as guiElementsWindow
from pygame._sdl2 import Window as SDLWindow

class Window(guiElementsWindow):
    def __init__(self, size: tuple, fps: int, title: str = "App", maximize: bool = False) -> None:
        super().__init__(size, fps, title)

        self.is_maximized = maximize

        if maximize:
            self.maximize()


    def maximize(self):
        """Maximizes the window
        """
        SDLWindow.from_display_module().maximize()

    def get_fps(self):
        """Returns the current frame rate

        Returns:
            float: the current frame rate
        """
        return self.clock.get_fps()
