from pygame.time import get_ticks
from pygame.key import get_pressed
from pygame import K_a, K_d

from guiElements.window import Window, WindowEvent

from entities import Player
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

        self.colliders.append(Block((0,400), (800, 200)))
        self.colliders.append(Block((0,0), (50, 400)))
        self.colliders.append(Block((750,0), (50, 400)))


        self.player = Player((60,250))
        self.player.set_pos((400,300))




    def update_display(self):
        """Updates the pygame display and renders objects on screen
        """

        # fill the canvas with white
        self.root.fill("white")

        self.player.blit(self.root.canvas)
        self.player.show_hitbox(self.root.canvas)


        for collider in self.colliders:
            collider.show_hitbox(self.root.canvas)


        self.root.update()


    
    def mainloop(self):
        """Main loop of the game
        """

        while self.events.getEvent("windowState"):
            self.root.tick()
            time = get_ticks()

            # update the events
            self.events.eventsCheck()


            keys = get_pressed()

            if keys[K_a]:
                if self.player.acc.x >= 0:
                    self.player.apply_force((-10,0))
            if keys[K_d]:
                if self.player.acc.x <= 0:
                    self.player.apply_force((10,0))


            self.player.update(self.colliders, time)

            self.update_display()