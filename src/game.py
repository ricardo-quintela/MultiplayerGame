import logging
from guiElements.inputs import Label
from pygame.draw import circle
from pygame import Surface
from pygame.transform import scale

from window import Window
from events import GameEvents
from utils import MovementKeys

from entities import Player

from config import MAPS
from maps import Map


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
        self.map = Map()

        # player
        self.player = Player((30,250))
        self.player.set_pos((900,400))
        self.player.current_room.update(self.map.map_size // 2, self.map.map_size // 2)






    def update_display(self):
        """Updates the pygame display and renders objects on screen
        """

        #! BACKGROUND
        # fill the canvas with white
        self.canvas.fill("white")

        # getting the current room
        current_map_room = self.map.get_room(self.player.current_room)

        # TODO: SET AS ROOM DEPENDANT
        #! ENEMIES
        for enemy in current_map_room.enemies:
            enemy.blit(self.canvas)
            enemy.show_bounding_box(self.canvas)


        #! PLAYER
        self.player.blit(self.canvas)
        self.player.show_bounding_box(self.canvas)


        #! DRAWING THE ROOM BLOCKS
        self.canvas.blit(current_map_room.block_layer, (0,0))


        #! SHOWING THE COLLIDERS (DEBUG)
        current_map_room.show_bounding_boxes(self.canvas)

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


            #! MAP
            current_map_room = self.map.get_room(self.player.current_room)

            #! ENEMIES
            for enemy in current_map_room.enemies:
                enemy.update(current_map_room.colliders, self.player)


            #! PLAYER
            self.player.move(movement_keys)
            self.player.update(current_map_room.colliders)

            #! MAP NAVIGATION
            if self.player.bounding_box.right < 0 and self.map.get_room(self.player.current_room + (-1,0)) is not None:
                self.player.current_room += (-1,0)
                self.player.set_pos((MAPS["room_size"][0] - self.player.bounding_box.width, self.player.pos.y))

            elif self.player.bounding_box.left > MAPS["room_size"][0] and self.map.get_room(self.player.current_room + (1,0)) is not None:
                self.player.current_room += (1,0)
                self.player.set_pos((self.player.bounding_box.width, self.player.pos.y))

            elif self.player.bounding_box.top > MAPS["room_size"][1] and self.map.get_room(self.player.current_room + (0,1)) is not None:
                self.player.current_room += (0,1)
                self.player.set_pos((self.player.pos.x, self.player.bounding_box.height))

            elif self.player.bounding_box.bottom < 0 and self.map.get_room(self.player.current_room + (0,-1)) is not None:
                self.player.current_room += (0,-1)
                self.player.set_pos((self.player.pos.x, 0))
                self.player.vel.y -= 10



            self.fps_counter.setText(f"FPS: {self.root.get_fps():.0f}", (0,0,0))

            self.update_display()
