import pygame
from .Global_Cache import Cache

def mouse_position():
    return pygame.mouse.get_pos()

def mouse_set_position(pos):
    pygame.mouse.set_pos(pos)

def mouse_set_visible(visible: bool = True):
    pygame.mouse.set_visible(visible)

def mouse_button(button: int = 1, multiple_click: bool = False):
    for num in range(5):
        if button - 1 == num:
            if pygame.mouse.get_pressed(5)[num]:
                if not Cache.Temp.Mouse["button_cache"][num] or multiple_click:
                    Cache.Temp.Mouse["button_cache"][num] = True
                    return True

        if not pygame.mouse.get_pressed(5)[num]:
            Cache.Temp.Mouse["button_cache"][num] = False
