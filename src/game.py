from guiElements.window import Window, WindowEvent

from utils import load_skeleton

class Game:

    def __init__(self, root: Window, events: WindowEvent) -> None:
        self.root = root
        self.events = events


        self.bones = load_skeleton("skeleton.json")


    def update_display(self):
        # fill the canvas with white
        self.root.fill("white")


        for bone in self.bones:
            bone.blit(self.root.canvas)


        self.root.update()


    
    def mainloop(self):

        while self.events.getEvent("windowState"):
            self.root.tick()

            # update the events
            self.events.eventsCheck()

            self.update_display()