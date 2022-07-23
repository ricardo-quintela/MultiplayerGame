import pygame

from guiElements.window import Window, WindowEvent

from game import Game

from config import WINDOW


def main():
    pygame.init()
    root = Window(WINDOW["SIZE"], WINDOW["FPS"])

    events = WindowEvent()

    game = Game(root, events)
    game.mainloop()

    pygame.quit()


if __name__ == "__main__":
    main()