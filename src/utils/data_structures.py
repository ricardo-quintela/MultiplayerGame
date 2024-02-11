from typing import TypedDict


class MovementKeys(TypedDict):
    left: bool
    right: bool
    jump: bool

class AttackKeys(TypedDict):
    attack: bool
    guard: bool
