from math import cos, sin
from pygame import Surface, Vector2
from config import ENTITIES

from utils import load_skeleton
from .entity import Entity

class Player(Entity):
    def __init__(self, hitbox_size) -> None:
        """Constructor of the class Player
        """
        super().__init__(hitbox_size, hasGravity=True)
        
        self.model = load_skeleton("skeleton.json")


        self.lerp_l = Vector2(self.pos)
        self.lerp_r = Vector2(self.pos)

        self.current_leg = 0

        self.legs = [self.lerp_l, self.lerp_r]

        self.target_leg_pos = Vector2(self.pos)


    
    def move_legs(self):
        self.target_leg_pos.update(self.pos + (self.direction * (self.hitbox.width / 2), 0))

        legs = ["coxa_e", "perna_e", "coxa_d", "perna_d"]

        distance = (self.model.getBone(legs[self.current_leg*2 + 1]).b - self.model.getBone(legs[self.current_leg * 2]).a).length()

        if distance >= (self.model.getBone(legs[self.current_leg * 2]).length + self.model.getBone(legs[self.current_leg * 2 + 1]).length):
            self.legs[self.current_leg].update(self.target_leg_pos)
            self.current_leg = (self.current_leg + 1) % 2




    def calculate_center(self):
        """Updates the center coordinate of the bone
        """
        tronco = self.model.getBone("tronco")
        self.model_center.update(tronco.a.x + cos(tronco.angle) * (tronco.length / 2), tronco.a.y + sin(tronco.angle) * (tronco.length / 2))



    def move(self, movement_keys: dict):
        """Checks for movement input and gives the player a velocity vector based on the movement direction

        Args:
            movement_keys (dict): the movement keys that are being pressed
        """
        if movement_keys["left"]:
            super().move((-5,0))
        if movement_keys["right"]:
            super().move((5,0))

        if not (movement_keys["left"] or movement_keys["right"]):
            self.isMoving = False


        if not self.isJumping and movement_keys["jump"]:
            super().move((0,-ENTITIES["JUMP_HEIGHT"]))
            self.isJumping = True





    def update(self, colliders: list):
        """Makes the necessary computations to update the physics of the player
        """
        vector = self.model.origin - self.model.getBone("tronco").a

        # calculate position based on velocity
        super().update()


        self.check_collisions(colliders)

        self.move_legs()


        #? updates the player model bones

        # move the origin of the model to the position of the hitbox and update the anchor bone as well
        self.model.set_origin(self.pos)
        self.model.getBone("tronco").a.update(self.model.origin - vector)

        # make the limbs follow specific points
        self.model.getLimb("coxa_e").follow(self.lerp_l, self.direction)
        self.model.getLimb("coxa_d").follow(self.lerp_r, self.direction)
        self.model.getLimb("antebraco_e").follow(self.hitbox.midleft)
        self.model.getLimb("antebraco_d").follow(self.hitbox.midright)

        # update the skeleton object
        self.model.update()


    def blit(self, canvas: Surface):
        """Draws the player model on the given surface

        Args:
            canvas (Surface): the surface where to draw the player on
        """

        self.model.blit(canvas)