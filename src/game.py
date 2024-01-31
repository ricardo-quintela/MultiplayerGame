import logging
from guiElements.inputs import Label
from pygame.draw import circle
from pygame import Surface
from json import loads
from pygame.transform import scale

from window import Window
from events import GameEvents
from utils import MovementKeys

from entities import Player

from config import MAPS
from maps import Room


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

        self.canvas = Surface(MAPS["room_size"])

        self.fps_counter = Label(f"FPS: {self.root.get_fps():.0f}", (0,0,0), 20)

        logging.info("Loading game assets")


        # map
        room_name = MAPS["rooms_folder"] + "test_room.json"
        with open(room_name, "r", encoding="utf-8") as room_file:
            self.room = Room.from_json(room_name, loads(room_file.read()))


        self.player = Player((30,250))
        self.player.set_pos((400,400))




    def update_display(self):
        """Updates the pygame display and renders objects on screen
        """

        #! BACKGROUND
        # fill the canvas with white
        self.canvas.fill("white")

        #! PLAYER
        self.player.blit(self.canvas)
        self.player.show_bounding_box(self.canvas)


        #! COLLIDERS
        self.room.show_bounding_boxes(self.canvas)

        #* DEBUGGING
        circle(self.canvas, "green", self.player.model.origin, 4)
        circle(self.canvas, "green", self.player.model.get_bone("tronco").a, 4)


        # transforming the canvas to match the screen size
        self.root.blit(scale(self.canvas, self.root.canvas.get_size()), (0,0))


        # show an FPS counter
        self.fps_counter.blit(self.root.canvas, (0,0))

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
            self.player.update(self.room.colliders)


            self.fps_counter.setText(f"FPS: {self.root.get_fps():.0f}", (0,0,0))

            self.update_display()
