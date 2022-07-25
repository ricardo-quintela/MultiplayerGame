from guiElements.window import Window
from events import GameEvents

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

        self.colliders.append(Block((0,400), (800, 200), 1))
        self.colliders.append(Block((0,0), (50, 400), 1))
        self.colliders.append(Block((750,0), (50, 400), 1))


        self.player = Player((60,250))
        self.player.set_pos((400,300))




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


        self.root.update()


    
    def mainloop(self):
        """Main loop of the game
        """

        while self.events.getEvent("windowState"):
            self.root.tick()

            #! EVENTS
            self.events.eventsCheck()
            movement_keys = {
                "left": self.events.keyIsPressed("a"),
                "right": self.events.keyIsPressed("d"),
                "jump": self.events.keyIsPressed("space")
                }


            #! PLAYER
            self.player.move(movement_keys)
            self.player.update(self.colliders)

            self.update_display()