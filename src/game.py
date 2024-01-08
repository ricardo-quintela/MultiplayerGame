import logging
from guiElements.window import Window
from events import GameEvents
from utils import MovementKeys

from config import ANIMATIONS

from pygame.draw import circle

from entities import Player
from blocks import Block


class Game:

    def __init__(self, root: Window, events: GameEvents) -> None:
        """Constructor of the class Game

        This class is ment to handle the rendering as well as the computations like collisions

        Args:
            root (Window): the window objecto
            events (GameEvents): the window events object
        """
        self.root = root
        self.events = events

        self.colliders = list()

        # map
        self.colliders.append(Block((0,400), (800, 200), 1))
        self.colliders.append(Block((0,0), (50, 400), 1))
        self.colliders.append(Block((750,0), (50, 400), 1))
        self.colliders.append(Block((500,370), (60, 30), 1))


        self.player = Player((30,250)) # default 60,250
        self.player.set_pos((400,400))




    def update_display(self):
        """Updates the pygame display and renders objects on screen
        """

        #! BACKGROUND
        # fill the canvas with white
        self.root.fill("white")

        #! PLAYER
        self.player.blit(self.root.canvas)
        self.player.show_hitbox(self.root.canvas)


        #! COLLIDERS
        for collider in self.colliders:
            collider.show_hitbox(self.root.canvas)

        #* DEBUGGING
        circle(self.root.canvas, "green", self.player.leg_targets[self.player.current_swing_leg], 4)
        circle(self.root.canvas, "green", self.player.pos, ANIMATIONS["LEG_TARGET"], 1)
        # circle(self.root.canvas, "blue", self.player.lerp_l, 4)
        # circle(self.root.canvas, "cyan", self.player.lerp_r, 4)

        # for k in self.player.keyframes:
        #     circle(self.root.canvas, "orange", k, 4)

        # circle(self.root.canvas, "black", self.player.leg_targets[self.player.current_swing_leg], 4)

        self.root.update()



    def mainloop(self):
        """Main loop of the game
        """

        while self.events.getEvent("windowState"):
            self.root.tick()

            #! EVENTS
            self.events.eventsCheck()
            movement_keys: MovementKeys = {
                "left": self.events.keyIsPressed("a"),
                "right": self.events.keyIsPressed("d"),
                "jump": self.events.keyIsPressed("space")
            }


            #! PLAYER
            self.player.move(movement_keys)
            self.player.update(self.colliders)

            self.update_display()
