from math import cos, sin
from pygame import Surface, Vector2

from utils import load_skeleton
from .entity import Entity


class Player(Entity):
    def __init__(self, hitbox_size) -> None:
        """Constructor of the class Player
        """
        super().__init__(hitbox_size, hasGravity=True)
        
        self.model = load_skeleton("skeleton.json")



    def calculate_center(self):
        """Updates the center coordinate of the bone
        """
        tronco = self.model.getBone("tronco")
        self.model_center.update(tronco.a.x + cos(tronco.angle) * (tronco.length / 2), tronco.a.y + sin(tronco.angle) * (tronco.length / 2))


    def update(self, colliders: list, time: int):
        """Makes the necessary computations to update the physics of the player
        """
        vector = self.model.origin - self.model.getBone("tronco").a

        super().update(time)

        self.check_collisions(colliders)

        self.model.set_origin(self.pos)
        self.model.getBone("tronco").a.update(self.model.origin - vector)

        self.model.getLimb("coxa_e").follow(self.hitbox.bottomleft)
        self.model.getLimb("coxa_d").follow(self.hitbox.bottomright)
        self.model.getLimb("antebraco_e").follow(self.hitbox.midleft)
        self.model.getLimb("antebraco_d").follow(self.hitbox.midright)

        self.model.update()


    def blit(self, canvas: Surface):
        """Draws the player model on the given surface

        Args:
            canvas (Surface): the surface where to draw the player on
        """

        self.model.blit(canvas)