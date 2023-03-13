import pygame
import threading
from .Keyboard import keyboard
from .Global_Cache import Cache
from .Key_Maps import Key_Input_Map
from .Platform import Platform

if not Platform.system == "Android":
    import pyperclip

class ObjectText:
    def __init__(self, localization, size: int, text: str = "", font=pygame.font.get_default_font()):
        self.localization = localization
        self.size = size

        self.font = font
        self.color = (255, 255, 255)
        self.text = text

        self.threading = threading.Thread(target=self.render())

        self.text_render_cache = False

        self.cursor = 11

        self.text_render = None
        self.text_render_font = None
        self.text_render_size = None

    def set_font(self, font):
        if self.font == font:
            pass
        else:
            self.font = font

    def set_color(self, color):
        if self.color == color:
            pass
        else:
            self.color = color
            self.text_render_cache = False

    def set_text(self, text: str):
        if self.text == text:
            pass
        else:
            self.text = text
            self.text_render_cache = False

    def set_localization(self, localization):
        if self.localization == localization:
            pass
        else:
            self.localization = localization
            self.text_render_cache = False

    def set_size(self, size: int):
        if self.size == size:
            pass
        else:
            self.size = size
            self.text_render_cache = False

    def set_loc_siz(self, localization, size):
        if self.size == size:
            pass
        else:
            self.size = size
            self.text_render_cache = False
        if self.localization == localization:
            pass
        else:
            self.localization = localization
            self.text_render_cache = False

    def get_text(self):
        return self.text

    def get_text_size(self):
        if self.text_render_cache:
            pass
        else:
            self.render()
        return self.text_render_size

    def threading_render(self):
        self.threading = threading.Thread(target=self.render())
        self.threading.start()

    def render(self):
        self.text_render_font = pygame.font.SysFont(self.font, self.size)
        self.text_render_size = self.text_render_font.size(self.text)
        self.text_render = self.text_render_font.render(self.text, True, self.color)
        self.text_render_cache = True

    def draw_object(self, screen, render: bool):
        loc_camera = screen.camera.get_location()
        size_screen = screen.screen.get_size()
        cache_screen_localization = [0, 0]
        cache_size = self.size
        cache_localization = self.localization

        if screen.__Window_Type__ == "Internal":
            cache_screen_size = screen.size
            cache_screen_localization = screen.localization

            for number in range(2):
                if "%" in str(cache_screen_size[number]):
                    cache_screen_size[number] = size_screen[number] / 100 * int(str(cache_screen_size[number]).replace("%", ""))

            for number in range(2):
                if "%" in str(cache_screen_localization[number]):
                    cache_screen_localization[number] = size_screen[number] / 100 * int(str(cache_screen_localization[number]).replace("%", ""))
                elif cache_screen_localization[number] == "center_obj":
                    cache_screen_localization[number] = (size_screen[number] - cache_screen_size[number]) / 2

        if "%" in str(cache_size):
            cache_size = size_screen[0] / 100 * int(str(cache_size).replace("%", ""))

        for number in range(2):
            if "%" in str(cache_localization[number]):
                cache_localization[number] = size_screen[number] / 100 * int(str(cache_localization[number]).replace("%", ""))
            elif cache_localization[number] == "center_obj":
                cache_localization[number] = (size_screen[number] - self.text_render_size[number]) / 2

        cache_localization = [cache_localization[0] + loc_camera[0] + cache_screen_localization[0], cache_localization[1] + loc_camera[1] + cache_screen_localization[1]]

        if not self.threading.is_alive():
            if render:
                if self.text:
                    if self.text_render_cache:
                        screen.screen.blit(self.text_render, (cache_localization[0], cache_localization[1]))
                    else:
                        self.threading_render()
                        if self.text_render_cache:
                            screen.screen.blit(self.text_render, (cache_localization[0], cache_localization[1]))
                else:
                    pass
            else:
                if not self.text_render_cache:
                    pass
                if self.text:
                    screen.screen.blit(self.text_render, (cache_localization[0], cache_localization[1]))

class ObjectTextBox:
    def __init__(self):
        pass

def text_box(text: str, type: str = "all", copy_and_paste: bool = True):
    if type == "all":
        set_text = list(Key_Input_Map.keys())
    elif type == "number":
        set_text = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "period"]
    else:
        print(f"Error (unrecognized_type)")
        return ""

    if copy_and_paste and not Platform.system == "Android":
        if keyboard("ctrl"):
            if keyboard("v"):
                if Cache.Temp.Keyboard["key_v_cache"]["press"]:
                    text += pyperclip.paste()
                    Cache.Temp.Keyboard["key_v_cache"]["press"] = False
                    return "".join(text)
            else:
                Cache.Temp.Keyboard["key_v_cache"]["press"] = True
            if keyboard("c"):
                if Cache.Temp.Keyboard["key_c_cache"]["press"]:
                    pyperclip.copy(text)
                    Cache.Temp.Keyboard["key_c_cache"]["press"] = False
                    return "".join(text)
            else:
                Cache.Temp.Keyboard["key_c_cache"]["press"] = True

    for key in set_text:
        cache_key = Key_Input_Map[key]
        if keyboard(key):
            if Cache.Temp.Keyboard[cache_key]["press"]:
                if key == "space":
                    text += " "
                    Cache.Temp.Keyboard[cache_key]["press"] = False
                elif key == "period":
                    text += "."
                    Cache.Temp.Keyboard[cache_key]["press"] = False
                else:
                    if pygame.key.get_mods() & 8192:
                        if keyboard("shift"):
                            text += key.lower()
                        else:
                            text += key.upper()
                    else:
                        if keyboard("shift"):
                            text += key.upper()
                        else:
                            text += key.lower()
                    Cache.Temp.Keyboard[cache_key]["press"] = False
        else:
            Cache.Temp.Keyboard[cache_key]["press"] = True

    if keyboard("back"):
        if Cache.Temp.Keyboard["key_backspace_cache"]["press"] or Cache.Temp.Keyboard["key_backspace_cache"]["time"] == 100:
            text = text[:-1]
            Cache.Temp.Keyboard["key_backspace_cache"]["press"] = False
        else:
            Cache.Temp.Keyboard["key_backspace_cache"]["time"] += 1
    else:
        Cache.Temp.Keyboard["key_backspace_cache"]["press"] = True
        Cache.Temp.Keyboard["key_backspace_cache"]["time"] = 0

    return "".join(text)
