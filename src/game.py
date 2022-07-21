from guiElements.window import Window, WindowEvent

from player import Player

class Game:

    def __init__(self, root: Window, events: WindowEvent) -> None:
        self.root = root
        self.events = events

        self.player = Player()


    def update_display(self):
        # fill the canvas with white
        self.root.fill("white")


        self.player.blit(self.root.canvas)


        self.root.update()


    
    def mainloop(self):

        while self.events.getEvent("windowState"):
            self.root.tick()

            # update the events
            self.events.eventsCheck()

            self.player.update()

            self.update_display()