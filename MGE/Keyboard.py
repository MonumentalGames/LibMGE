import pygame
from .Key_Maps import Key_Map

def keyboard(key):
    key = str(key).lower()
    event_key = pygame.key.get_pressed()

    if key == "all":
        return any(event_key)

    if key in Key_Map:
        if isinstance(Key_Map[key], int):
            return event_key[Key_Map[key]]
        else:
            return any(event_key[k] for k in Key_Map[key])

    return False
