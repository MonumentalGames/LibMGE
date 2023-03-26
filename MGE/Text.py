import pygame
import threading
import sys
from .MGE import Program
from .Keyboard import keyboard
from .Global_Cache import Cache
from .Key_Maps import Key_Map
from .Platform import Platform

if not Platform.system == "Android":
    import pyperclip

class ObjectText:
    def __init__(self, localization, size: int, text: str = "", font=Program.default_font):
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
        self.text_render_size = [0, 0]

    def set_font(self, font):
        if not self.font == font:
            self.font = font

    def set_color(self, color):
        if not self.color == color:
            self.color = color
            self.text_render_cache = False

    def set_text(self, text: str):
        if not self.text == text:
            self.text = text
            self.text_render_cache = False

    def set_localization(self, localization):
        if not self.localization == localization:
            self.localization = localization
            self.text_render_cache = False

    def set_size(self, size: int):
        if not self.size == size:
            self.size = size
            self.text_render_cache = False

    def set_loc_siz(self, localization, size):
        if not self.size == size:
            self.size = size
            self.text_render_cache = False
        if not self.localization == localization:
            self.localization = localization
            self.text_render_cache = False

    def get_text(self):
        return self.text

    def get_text_size(self):
        if not self.text_render_cache:
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

    def draw_object(self, screen, camera=None, render: bool = True):
        if camera is not None:
            loc_camera = camera.get_location()
        else:
            loc_camera = screen.camera.get_location()
        size_screen = screen.screen.get_size()
        cache_screen_localization = [0, 0]
        cache_localization = list(self.localization)

        if screen.__Window_Type__ == "Internal":
            cache_screen_localization = screen.get_localization()

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
                        screen.screen.blit(self.text_render, cache_localization)
                    else:
                        self.threading_render()
                        if self.text_render_cache:
                            screen.screen.blit(self.text_render, cache_localization)
            else:
                if self.text:
                    if self.text_render_cache:
                        screen.screen.blit(self.text_render, cache_localization)

class ObjectTextBox:
    def __init__(self, localization, size: int, text: str = "", default_text: str = "", font=Program.default_font):
        self.localization = localization
        self.default_text = default_text
        self.text = text
        self.cache_texts = []

        self.limit_size = None
        self.limit_size_pix = None

        self.type = "all"

        self.copy_and_paste = True

        self.ObjectText = ObjectText(localization, size, self.text, font)

    def input_text(self, key, cache_key):
        if "kp" in key:
            key = key.replace("kp", "")
        if key == "space":
            self.text += " "
            Cache.Temp.Keyboard[cache_key]["press"] = False
        elif key == "period":
            self.text += "."
            Cache.Temp.Keyboard[cache_key]["press"] = False
        else:
            if pygame.key.get_mods() & 8192:
                if keyboard("shift"):
                    self.text += key.lower()
                else:
                    self.text += key.upper()
            else:
                if keyboard("shift"):
                    self.text += key.upper()
                else:
                    self.text += key.lower()
            Cache.Temp.Keyboard[cache_key]["press"] = False

    def update(self):
        if self.type == "all":
            set_text = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "kp1", "kp2", "kp3", "kp4", "kp5", "kp6", "kp7", "kp8", "kp9", "kp0", "period",
                        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                        "space"]
        elif self.type == "number":
            set_text = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "kp1", "kp2", "kp3", "kp4", "kp5", "kp6", "kp7", "kp8", "kp9", "kp0", "period"]
        else:
            sys.exit(f"MGE-Error (unrecognized_type)")

        if len(self.cache_texts) >= 25:
            self.cache_texts = self.cache_texts[1:]

        if self.limit_size is None:
            cache_limit_size = 9999999
        else:
            cache_limit_size = self.limit_size
        if len(self.text) < cache_limit_size:
            if self.copy_and_paste and not Platform.system == "Android":
                if keyboard("ctrl"):
                    if keyboard("v"):
                        if Cache.Temp.Keyboard["key_v_cache"]["press"]:
                            self.text += pyperclip.paste()
                            Cache.Temp.Keyboard["key_v_cache"]["press"] = False
                    else:
                        Cache.Temp.Keyboard["key_v_cache"]["press"] = True
                    if keyboard("c"):
                        if Cache.Temp.Keyboard["key_c_cache"]["press"]:
                            pyperclip.copy(self.text)
                            Cache.Temp.Keyboard["key_c_cache"]["press"] = False
                    else:
                        Cache.Temp.Keyboard["key_c_cache"]["press"] = True

            for key in set_text:
                cache_key = Key_Map[key]["cache"]
                if keyboard(key):
                    if Cache.Temp.Keyboard[cache_key]["press"] or Cache.Temp.Keyboard[cache_key]["time"]["press"] == 100:
                        if Cache.Temp.Keyboard[cache_key]["time"]["press"] == 100:
                            if Cache.Temp.Keyboard[cache_key]["time"]["loop"] >= Program.get_fps() / 30:
                                self.input_text(key, cache_key)
                                Cache.Temp.Keyboard[cache_key]["time"]["loop"] = 0
                            Cache.Temp.Keyboard[cache_key]["time"]["loop"] += 1
                        else:
                            self.input_text(key, cache_key)
                    else:
                        Cache.Temp.Keyboard[cache_key]["time"]["press"] += 1
                else:
                    if not Cache.Temp.Keyboard[cache_key]["press"]:
                        self.cache_texts.append(self.text)
                    Cache.Temp.Keyboard[cache_key]["press"] = True
                    Cache.Temp.Keyboard[cache_key]["time"]["press"] = 0

        if keyboard("back"):
            if Cache.Temp.Keyboard["key_backspace_cache"]["press"] or Cache.Temp.Keyboard["key_backspace_cache"]["time"]["press"] == 100:
                if Cache.Temp.Keyboard["key_backspace_cache"]["time"]["press"] == 100:
                    if Cache.Temp.Keyboard["key_backspace_cache"]["time"]["loop"] >= Program.get_fps() / 30:
                        self.text = self.text[:-1]
                        Cache.Temp.Keyboard["key_backspace_cache"]["press"] = False
                        Cache.Temp.Keyboard["key_backspace_cache"]["time"]["loop"] = 0
                    Cache.Temp.Keyboard["key_backspace_cache"]["time"]["loop"] += 1
                else:
                    self.text = self.text[:-1]
                    Cache.Temp.Keyboard["key_backspace_cache"]["press"] = False
            else:
                Cache.Temp.Keyboard["key_backspace_cache"]["time"]["press"] += 1
        else:
            if not Cache.Temp.Keyboard["key_backspace_cache"]["press"]:
                self.cache_texts.append(self.text)
            Cache.Temp.Keyboard["key_backspace_cache"]["press"] = True
            Cache.Temp.Keyboard["key_backspace_cache"]["time"]["press"] = 0

        if self.limit_size_pix is not None:
            if not self.ObjectText.get_text_size()[0] >= self.limit_size_pix or len(self.text) < len(self.ObjectText.text):
                self.ObjectText.set_text(self.text)
            else:
                self.text = self.ObjectText.text
        else:
            self.ObjectText.set_text(self.text)

    def draw_object(self, screen, camera=None, render: bool = True):
        self.ObjectText.draw_object(screen, camera, render)

    def clean_cache(self):
        self.cache_texts.clear()
