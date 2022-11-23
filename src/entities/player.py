from math import sqrt, sin, cos
from pygame import Surface, Vector2
from pygame.time import get_ticks
from config import ENTITIES, ANIMATIONS

from utils import load_skeleton
from .entity import Entity

class Player(Entity):
    def __init__(self, hitbox_size) -> None:
        """Constructor of the class Player
        """
        super().__init__(hitbox_size, has_gravity=True)
        
        self.model = load_skeleton("skeleton.json")


        self.lerp_l = Vector2(self.pos)
        self.lerp_r = Vector2(self.pos)

        self.leg_l = Vector2(self.pos)
        self.leg_r = Vector2(self.pos)

        self.hip = self.model.getLimb("coxa_e").anchor

        self.current_leg = 0

        self.lerps = [self.lerp_l, self.lerp_r]
        self.legs = [self.leg_l, self.leg_r]

        self.target_leg_pos = Vector2(self.pos)

        self.keyframes = list()
        self.current_keyframe = 0
        self.last_keyframe_time = 0


    
    def move_legs(self, colliders: list):


        # cap the leg positioning
        for leg in self.legs:
            if leg.y < self.pos.y - ANIMATIONS["LEG_TARGET_HEIGHT"]:
                leg.y = self.pos.y - ANIMATIONS["LEG_TARGET_HEIGHT"]

            if self.current_leg == 0 and leg.y < self.pos.y:
                leg.y = self.pos.y


        #! RAYCAST OF TARGET POS
        # start of the player leg target position
        self.target_leg_pos.update(self.pos + (self.direction * ANIMATIONS["LEG_TARGET"], -ANIMATIONS["LEG_TARGET_HEIGHT"]))

        # ray cast the target position until it reaches the limit of the hitbox
        while self.target_leg_pos.y < self.pos.y:

            # check collisions of the target point for each object
            for block in colliders:


                # if the point collides with an object and its top is between the allowed step height set the target position to the top of the block
                if block.hitbox.collidepoint(self.target_leg_pos) and block.hitbox.top >= self.pos.y - ANIMATIONS["LEG_TARGET_HEIGHT"]:
                    self.target_leg_pos.y = block.hitbox.top
                    break # break the for loop


            else: # update the target y position if the for loop completes without breaking
                self.target_leg_pos.y += ANIMATIONS["LEG_SCANNER_STEP"]
                continue # continue the while loop
            
            break # break if the program doesnt enter else

        # se a distancia da anca até ao pe for menor que o tamanho da perna: lerp = target pos
        
        if (self.hip - self.legs[self.current_leg]).length() > self.model.getLimb("coxa_e").size:

            self.lerps[self.current_leg].update(self.target_leg_pos)
            self.current_leg = (self.current_leg + 1) % 2


        if self.legs[self.current_leg] < self.lerps[self.current_leg]:
            self.legs[self.current_leg] += (self.direction * 100, 0)







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


        if not self.is_jumping and movement_keys["jump"]:
            super().move((0,-ENTITIES["JUMP_HEIGHT"]))
            self.is_jumping = True





    def update(self, colliders: list):
        """Makes the necessary computations to update the physics of the player
        """
        vector = self.model.origin - self.model.getBone("tronco").a

        # calculate position based on velocity
        super().update()


        self.check_collisions(colliders)

        self.move_legs(colliders)


        #? updates the player model bones

        # move the origin of the model to the position of the hitbox and update the anchor bone as well
        self.model.set_origin(self.pos)
        self.model.getBone("tronco").a.update(self.model.origin - vector)

        # make the limbs follow specific points
        self.model.getLimb("coxa_e").follow(self.leg_l, self.direction)
        self.model.getLimb("coxa_d").follow(self.leg_r, self.direction)
        self.model.getLimb("antebraco_e").follow(self.hitbox.midleft, -self.direction)
        self.model.getLimb("antebraco_d").follow(self.hitbox.midright, -self.direction)

        # update the skeleton object
        self.model.update()


    def blit(self, canvas: Surface):
        """Draws the player model on the given surface

        Args:
            canvas (Surface): the surface where to draw the player on
        """

        self.model.blit(canvas)