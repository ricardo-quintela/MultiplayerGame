from pygame import Rect, Surface, Vector2
from pygame.draw import rect


from config import PHYSICS, ENTITIES


class Entity:

    def __init__(self, hitbox_size: tuple, has_gravity: bool = True, max_vel_x: int = ENTITIES["MAX_VEL_X"], max_vel_y: int = ENTITIES["MAX_VEL_Y"]) -> None:
        """Constructor of the class Entity

        Args:
            hitbox_size (tuple): the size of the hitbox
            hasGravity (bool): whether to enable gravity to the object or not. Defaults to True.
        """
        self.pos = Vector2(0,0)

        self.hitbox = Rect((0,0), hitbox_size)

        # velocity
        self.vel = Vector2(0,0)

        self.has_gravity = has_gravity
        self.max_vel_x = max_vel_x
        self.max_vel_y = max_vel_y

        self.is_moving = False
        self.is_jumping = False

        self.direction = 1


    def set_pos(self, pos: tuple):
        """Sets the pos of the entity's midbottom to the given set of coordinates

        Args:
            pos (tuple): the position where to place the hitbox on
        """
        self.pos.update(pos)


    def move(self, vel: tuple):
        """Gives the entity a given velocity vector\n

        Args:
            vel (tuple): the velocity vector to apply
        """
        self.vel.x += vel[0]
        self.vel.y += vel[1] if self.vel.y + vel[1] <= self.max_vel_y else 0

        # movement direction
        if vel[0] < 0:
            self.direction = -1
            if self.vel.x < -self.max_vel_x:
                self.vel.x = -self.max_vel_x
                
        elif vel[0] > 0:
            self.direction = 1
            if self.vel.x > self.max_vel_x:
                self.vel.x = self.max_vel_x

        self.is_moving = True


    def update(self):
        """Calculate the position based on the velocity
        """

        # updating the vellocity
        self.vel.y += PHYSICS["GRAVITY"]

        # updating the position
        self.pos += self.vel

        # update the hitbox pos values since it doesnt allow the link with a muttable object
        self.hitbox.midbottom = self.pos

        #print(self.pos, self.vel, self.acc, (self.hitbox.x, self.hitbox.y))



    def check_collisions(self, colliders: list):
        """Handles collisions between this entity and blocks on a given list

        Args:
            colliders (list): the list of colliders in the level
        """

        self.hitbox.center += self.vel

        # iterate through colliders
        for block in colliders:

            # found a collision
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
                    self.is_jumping = False
                    
                    # calculate friction when the entity is not moving
                    if not self.is_moving:

                        # friction
                        if self.vel.x < 0:
                            self.vel.x += block.friction
                        elif self.vel.x > 0:
                            self.vel.x -= block.friction


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


    def show_hitbox(self, canvas: Surface):
        """Draws a rectangle on the given canvas representing the hitbox of the entity

        Args:
            canvas (Surface): the canvas where to draw the rectangle on
        """

        rect(canvas, "blue", (self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)
    