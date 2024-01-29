# pylint: disable=maybe-no-member
import pygame
import logging

from window import Window
from events import GameEvents

from game import Game

from config import LOGGING, WINDOW


logging.basicConfig(
    format='[%(asctime)s] %(thread)s %(levelname)s :  %(message)s'
)
logging.getLogger().setLevel(LOGGING["level"])


def main():
    pygame.init()

    logging.debug("Building window")
    root = Window(WINDOW["size"], WINDOW["fps"], maximize=WINDOW["maximized"])

    logging.debug("Loading window events")
    events = GameEvents()

    logging.debug("Building game object")
    game = Game(root, events)

    logging.debug("Starting mainloop")
    game.mainloop()

    pygame.quit()


if __name__ == "__main__":
    logging.debug("Starting")
    main()
    logging.debug("Exited successfully")
