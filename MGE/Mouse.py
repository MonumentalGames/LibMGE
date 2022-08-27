import pygame
from .MGE import Cache

def mouse_position():
    return pygame.mouse.get_pos()

def mouse_button(button, multiple_click=False):
    if multiple_click:
        if button == 1:
            if pygame.mouse.get_pressed(3)[0]:
                return True
        if button == 2:
            if pygame.mouse.get_pressed(3)[1]:
                return True
        if button == 3:
            if pygame.mouse.get_pressed(3)[2]:
                return True
    else:
        if button == 1:
            if pygame.mouse.get_pressed(3)[0]:
                if not Cache.Mouse_Button.button_cache[0]:
                    Cache.Mouse_Button.button_cache[0] = True
                    return True
        if button == 2:
            if pygame.mouse.get_pressed(3)[1]:
                if not Cache.Mouse_Button.button_cache[1]:
                    Cache.Mouse_Button.button_cache[1] = True
                    return True
        if button == 3:
            if pygame.mouse.get_pressed(3)[2]:
                if not Cache.Mouse_Button.button_cache[2]:
                    Cache.Mouse_Button.button_cache[2] = True
                    return True

        if not pygame.mouse.get_pressed(3)[0]:
            Cache.Mouse_Button.button_cache[0] = False
        if not pygame.mouse.get_pressed(3)[1]:
            Cache.Mouse_Button.button_cache[1] = False
        if not pygame.mouse.get_pressed(3)[2]:
            Cache.Mouse_Button.button_cache[2] = False
