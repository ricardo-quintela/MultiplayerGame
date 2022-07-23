from pygame.time import get_ticks

from guiElements.window import Window, WindowEvent

from entities import Entity
from blocks import Block


class Game:

    def __init__(self, root: Window, events: WindowEvent) -> None:
        """Constructor of the class Game

        This class is ment to handle the rendering as well as the computations like collisions

        Args:
            root (Window): the window objecto
            events (WindowEvent): the window events object
        """
        self.root = root
        self.events = events

        self.colliders = list()



    def update_display(self):
        """Updates the pygame display and renders objects on screen
        """

        # fill the canvas with white
        self.root.fill("white")


        self.root.update()


    
    def mainloop(self):
        """Main loop of the game
        """

        while self.events.getEvent("windowState"):
            self.root.tick()
            time = get_ticks()

            # update the events
            self.events.eventsCheck()



            self.update_display()