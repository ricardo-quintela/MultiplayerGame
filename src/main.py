import pygame

from guiElements.window import Window
from events import GameEvents

from game import Game

from config import WINDOW


def main():
    pygame.init()
    root = Window(WINDOW["SIZE"], WINDOW["FPS"])

    events = GameEvents()

    game = Game(root, events)
    game.mainloop()

    pygame.quit()


if __name__ == "__main__":
    main()