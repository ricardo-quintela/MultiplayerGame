from pygame import Rect, Surface, Vector2
from pygame.draw import rect


from config import PHYSICS


class Entity:

    last_update: int = 0

    def __init__(self, hitbox_size: tuple, hasGravity: bool = True) -> None:
        """Constructor of the class Entity

        Args:
            hitbox_size (tuple): the size of the hitbox
            hasGravity (bool): whether to enable gravity to the object or not. Defaults to True.
        """
        self.pos = Vector2(0,0)

        self.hitbox = Rect((0,0), hitbox_size)

        # velocity
        self.vel = Vector2(0,0)

        # acceleration
        self.hasGravity = hasGravity 
        self.acc = Vector2(0,0)
        self.acc.y = PHYSICS["GRAVITY"]




    def set_pos(self, pos: tuple):
        """Sets the pos of the entity's midbottom to the given set of coordinates

        Args:
            pos (tuple): the position where to place the hitbox on
        """
        self.pos.update(pos)


    def apply_force(self, force: tuple):
        """Applies a force to the entity\n

        Affects acceleration and velocity in the initial instant

        Args:
            force (tuple): the force to apply to the entity
        """
        self.acc += force


    def update(self, time: int):
        """Calculate the position based on the acceleration
        """

        # updating the vellocity
        if time - Entity.last_update >= PHYSICS["SECOND"]:
            self.vel += self.acc
            Entity.last_update = time

        # updating the position
        self.pos += self.vel

        # update the hitbox pos values since it doesnt allow the link with a muttable object
        self.hitbox.midbottom = self.pos

        #print(self.pos, self.vel, self.acc, (self.hitbox.x, self.hitbox.y))



    def check_collisions(self, colliders: list):


        for block in colliders:

            if self.hitbox.colliderect(block.hitbox):

                # keys are block's sides
                distances = {
                    "top": abs(self.hitbox.bottom - block.hitbox.top),
                    "left": abs(self.hitbox.right - block.hitbox.left),
                    "right": abs(self.hitbox.left - block.hitbox.right),
                    "bottom": abs(self.hitbox.top - block.hitbox.bottom)
                }

                min_dist = min(distances, key=distances.get)

                # print("DISTS:", distances, "\nCOLLIDED: ", min_dist, sep="")

                # collision handeling
                if min_dist == "top":
                    self.hitbox.bottom = block.hitbox.top
                    self.vel.y = 0
                elif min_dist == "left":
                    self.hitbox.right = block.hitbox.left
                    self.vel.x = 0
                elif min_dist == "right":
                    self.hitbox.left = block.hitbox.right
                    self.vel.x = 0
                else:
                    self.hitbox.top = block.hitbox.bottom
                    self.vel.y = 0
                
                self.pos.update(self.hitbox.midbottom)



    def blit(self, canvas: Surface):
        """Draws a rectangle on the given canvas representing the hitbox of the entity

        Args:
            canvas (Surface): the canvas where to draw the rectangle on
        """

        rect(canvas, "blue", (self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)
    