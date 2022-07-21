from guiElements.window import Window, WindowEvent

from utils import load_skeleton

class Game:

    def __init__(self, root: Window, events: WindowEvent) -> None:
        self.root = root
        self.events = events

        self.skeleton = load_skeleton("skeleton.json")


    def update_display(self):
        # fill the canvas with white
        self.root.fill("white")


        self.skeleton.blit(self.root.canvas)


        self.root.update()


    
    def mainloop(self):

        pos = [100,100]
        m = 1

        while self.events.getEvent("windowState"):
            self.root.tick()

            # update the events
            self.events.eventsCheck()


            pos[0] += 5 * m

            if pos[0] <= 100 or pos[0] >= 600:
                m *= -1

            self.skeleton.getBone("4").set_pos(pos)

            self.skeleton.getLimb("6").follow(self.events.getEvent("mousePos"))

            self.skeleton.update()

            self.update_display()