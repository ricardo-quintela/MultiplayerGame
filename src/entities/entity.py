import logging
from typing import Dict, List, Union, Literal, Tuple
from pygame import Surface, Vector2
from pygame.draw import rect

from utils import BoundingBox
from blocks import Collider

from config import PHYSICS, ENTITIES, DEBUG


class Entity:
    """An entity handles basic physics calculations
    and movement. It's bounding_box can also be drawn on the screen
    """

    def __init__(self, bounding_box_size: tuple, has_gravity: bool = True, max_vel_x: int = ENTITIES["max_vel_x"], max_vel_y: int = ENTITIES["max_vel_y"]) -> None:
        """Constructor of the class Entity

        Args:
            bounding_box_size (tuple): the size of the bounding_box
            hasGravity (bool): whether to enable gravity to the object or not. Defaults to True.
        """
        self.pos = Vector2(0,0)

        self.bounding_box = BoundingBox((0,0), bounding_box_size)

        # velocity
        self.vel = Vector2(0,0)

        self.has_gravity = has_gravity
        self.max_vel_x = max_vel_x
        self.max_vel_y = max_vel_y

        # states
        self.is_colliding: bool = False
        self.is_moving: bool = False
        self.is_jumping: bool = False
        self.is_grounded: bool = False
        self.is_climbing: bool = False
        self.is_attacking: bool = False
        self.is_stunned: bool = False


        # attacking and combos
        self.attack_sequence: int = 0

        self.direction: Union[Literal[1], Literal[-1]] = 1


    def set_pos(self, pos: tuple):
        """Sets the pos of the entity's midbottom to the given set of coordinates

        Args:
            pos (tuple): the position where to place the bounding_box on
        """
        self.pos.update(pos)


    def move(self, vel: Tuple[int, int]):
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

    def calculate_position(self):
        """Calculates the new position based on the velocity
        also handles gravity calculations
        """
        # updating the vellocity
        if self.has_gravity and not self.is_climbing:
            logging.debug("GRAVITY_CALCULATION")
            self.vel.y += PHYSICS["gravity"]

        # updating the position
        self.pos += self.vel


    def update(self):
        """updates the position and the bounding box
        """
        self.calculate_position()

        # update the bounding_box pos values since it doesnt allow the link with a muttable object
        self.bounding_box.midbottom = self.pos

        logging.debug(
            "POS: %s, VEL: %s BOUNDING_BOX: (%s, %s)",
            self.pos,
            self.vel,
            self.bounding_box.x,
            self.bounding_box.y
        )



    def check_collisions(self, colliders: List[Collider]) -> Dict[str, Union[Collider, None]]:
        """Handles collisions between this entity and colliders on a given list

        Args:
            colliders (list): the list of colliders in the level

        Returns:
            Dict[str, Union[Collider, None]]: the colliders that the entity collided with
        """
        self.is_colliding = False
        self.is_grounded = False

        collisions = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None
        }

        # iterate through colliders
        for collider in colliders:

            # found a collision
            if self.bounding_box.colliderect(collider.bounding_box):
                self.is_colliding = True

                # keys are collider's sides
                distances = {
                    "top": abs(self.bounding_box.bottom - self.vel.y - collider.bounding_box.top),
                    "bottom": abs(self.bounding_box.top - self.vel.y - collider.bounding_box.bottom),
                    "left": abs(self.bounding_box.right - self.vel.x - collider.bounding_box.left),
                    "right": abs(self.bounding_box.left - self.vel.x - collider.bounding_box.right)
                }

                min_dist = min(distances, key=distances.get)

                logging.debug(
                    "DISTS: %s | COLLIDED: %s | BBOX LIST: %s",
                    distances,
                    min_dist,
                    {
                        "top": (self.bounding_box.bottom - self.vel.y, collider.bounding_box.top),
                        "bottom": (self.bounding_box.top - self.vel.y, collider.bounding_box.bottom),
                        "left": (self.bounding_box.right - self.vel.x, collider.bounding_box.left),
                        "right": (self.bounding_box.left - self.vel.x, collider.bounding_box.right)
                    }
                )

                # collision handling
                if min_dist == "top":
                    self.bounding_box.bottom = collider.bounding_box.top
                    self.vel.y = 0
                    self.is_jumping = False
                    self.is_grounded = True
                    collisions["top"] = collider

                    # calculate friction when the entity is not moving
                    if not self.is_moving:

                        # friction
                        if self.vel.x < 0:
                            self.vel.x = self.vel.x + collider.friction if self.vel.x + collider.friction < 0 else 0

                        elif self.vel.x > 0:
                            self.vel.x = self.vel.x - collider.friction if self.vel.x - collider.friction > 0 else 0

                elif min_dist == "left":
                    self.bounding_box.right = collider.bounding_box.left
                    self.vel.x = 0
                    collisions["left"] = collider
                elif min_dist == "right":
                    self.bounding_box.left = collider.bounding_box.right
                    self.vel.x = 0
                    collisions["right"] = collider
                else:
                    self.bounding_box.top = collider.bounding_box.bottom
                    self.vel.y = 0
                    collisions["bottom"] = collider

                self.pos.update(self.bounding_box.midbottom)

        return collisions


    def show_bounding_box(self, canvas: Surface):
        """Draws a rectangle on the given canvas representing the bounding_box of the entity

        Args:
            canvas (Surface): the canvas where to draw the rectangle on
        """

        rect(
            canvas,
            DEBUG["entity_bbox_color"],
            (self.bounding_box.x, self.bounding_box.y, self.bounding_box.width, self.bounding_box.height),
            2
        )
    