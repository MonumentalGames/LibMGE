import pygame
import pyperclip
import threading
from .Keyboard import keyboard
from .MGE import Cache

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
        if screen.get_screen_type() == "main":
            size_screen = screen.screen.get_size()
            cache_localization = self.localization

            if "%" in str(cache_localization[0]):
                cache_000 = str(cache_localization[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = (size_screen[0] / 100 * cache_000, cache_localization[1])
            if "%" in str(cache_localization[1]):
                cache_000 = str(cache_localization[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = [cache_localization[0], size_screen[1] / 100 * cache_000]

            if cache_localization[0] == "center_obj":
                cache_localization[0] = (size_screen[0] - self.text_render_size[0]) / 2
            if cache_localization[1] == "center_obj":
                cache_localization[1] = (size_screen[1] - self.text_render_size[1]) / 2

            try:
                cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
            except TypeError:
                print("Error")
                cache_localization = [0, 0]
        elif screen.get_screen_type() == "Internal":
            size_screen = screen.screen.get_size()

            cache_screen_size = screen.size
            cache_screen_localization = screen.localization

            cache_size = self.size
            cache_localization = self.localization

            if "%" in str(cache_screen_localization[0]):
                cache_000 = str(cache_screen_localization[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_localization = (size_screen[0] / 100 * cache_000, cache_screen_localization[1])
            if "%" in str(cache_screen_localization[1]):
                cache_000 = str(cache_screen_localization[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_localization = [cache_screen_localization[0], size_screen[1] / 100 * cache_000]

            if "%" in str(cache_screen_size[0]):
                cache_000 = str(cache_screen_size[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_size = (size_screen[0] / 100 * cache_000, cache_screen_size[1])
            if "%" in str(cache_screen_size[1]):
                cache_000 = str(cache_screen_size[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_screen_size = (cache_screen_size[0], size_screen[1] / 100 * cache_000)

            if cache_screen_localization[0] == "center_obj":
                cache_screen_localization[0] = (size_screen[0] - cache_screen_size[0]) / 2
            if cache_screen_localization[1] == "center_obj":
                cache_screen_localization[1] = (size_screen[1] - cache_screen_size[1]) / 2

            ##-----------------------------------------------------##

            if "%" in str(cache_localization[0]):
                cache_000 = str(cache_localization[0]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = (size_screen[0] / 100 * cache_000, cache_localization[1])
            if "%" in str(cache_localization[1]):
                cache_000 = str(cache_localization[1]).replace("%", "")
                cache_000 = int(cache_000)
                cache_localization = [cache_localization[0], size_screen[1] / 100 * cache_000]

            if cache_localization[0] == "center_obj":
                cache_localization[0] = (size_screen[0] - cache_size[0]) / 2
            if cache_localization[1] == "center_obj":
                cache_localization[1] = (size_screen[1] - cache_size[1]) / 2

            try:
                cache_localization = [cache_localization[0] + loc_camera[0], cache_localization[1] + loc_camera[1]]
                cache_localization = [cache_localization[0] + cache_screen_localization[0], cache_localization[1] + cache_screen_localization[1]]
            except TypeError:
                print("Error")
                cache_localization = screen.localization
        else:
            try:
                cache_localization = [self.localization[0] + loc_camera[0], self.localization[1] + loc_camera[1]]
            except TypeError:
                print("Error")
                cache_localization = [0, 0]

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

def text_box(text: str, type: str = "all"):
    if type == "all":
        set_text = [True, True, True]
    elif type == "number":
        set_text = [False, True, False]
    else:
        set_text = [False, False, False]

    if keyboard("ctrl"):
        if keyboard("v"):
            if Cache.Temp.Keyboard.key_v_cache:
                text += pyperclip.paste()
                Cache.Temp.Keyboard.key_v_cache = False
        else:
            Cache.Temp.Keyboard.key_v_cache = True

        if keyboard("c"):
            if Cache.Temp.Keyboard.key_c_cache:
                #text += pyperclip.paste()
                Cache.Temp.Keyboard.key_c_cache = False
        else:
            Cache.Temp.Keyboard.key_c_cache = True

    if set_text[0]:
        if keyboard("shift"):

            if keyboard("a"):
                if Cache.Temp.Keyboard.key_a_cache:
                    text += "A"
                    Cache.Temp.Keyboard.key_a_cache = False
            else:
                Cache.Temp.Keyboard.key_a_cache = True

            if keyboard("b"):
                if Cache.Temp.Keyboard.key_b_cache:
                    text += "B"
                    Cache.Temp.Keyboard.key_b_cache = False
            else:
                Cache.Temp.Keyboard.key_b_cache = True

            if keyboard("c"):
                if Cache.Temp.Keyboard.key_c_cache:
                    text += "C"
                    Cache.Temp.Keyboard.key_c_cache = False
            else:
                Cache.Temp.Keyboard.key_c_cache = True

            if keyboard("d"):
                if Cache.Temp.Keyboard.key_d_cache:
                    text += "D"
                    Cache.Temp.Keyboard.key_d_cache = False
            else:
                Cache.Temp.Keyboard.key_d_cache = True

            if keyboard("e"):
                if Cache.Temp.Keyboard.key_e_cache:
                    text += "E"
                    Cache.Temp.Keyboard.key_e_cache = False
            else:
                Cache.Temp.Keyboard.key_e_cache = True

            if keyboard("f"):
                if Cache.Temp.Keyboard.key_f_cache:
                    text += "F"
                    Cache.Temp.Keyboard.key_f_cache = False
            else:
                Cache.Temp.Keyboard.key_f_cache = True

            if keyboard("g"):
                if Cache.Temp.Keyboard.key_g_cache:
                    text += "G"
                    Cache.Temp.Keyboard.key_g_cache = False
            else:
                Cache.Temp.Keyboard.key_g_cache = True

            if keyboard("h"):
                if Cache.Temp.Keyboard.key_h_cache:
                    text += "H"
                    Cache.Temp.Keyboard.key_h_cache = False
            else:
                Cache.Temp.Keyboard.key_h_cache = True

            if keyboard("i"):
                if Cache.Temp.Keyboard.key_i_cache:
                    text += "I"
                    Cache.Temp.Keyboard.key_i_cache = False
            else:
                Cache.Temp.Keyboard.key_i_cache = True

            if keyboard("j"):
                if Cache.Temp.Keyboard.key_j_cache:
                    text += "J"
                    Cache.Temp.Keyboard.key_j_cache = False
            else:
                Cache.Temp.Keyboard.key_j_cache = True

            if keyboard("k"):
                if Cache.Temp.Keyboard.key_k_cache:
                    text += "K"
                    Cache.Temp.Keyboard.key_k_cache = False
            else:
                Cache.Temp.Keyboard.key_k_cache = True

            if keyboard("l"):
                if Cache.Temp.Keyboard.key_l_cache:
                    text += "L"
                    Cache.Temp.Keyboard.key_l_cache = False
            else:
                Cache.Temp.Keyboard.key_l_cache = True

            if keyboard("m"):
                if Cache.Temp.Keyboard.key_m_cache:
                    text += "M"
                    Cache.Temp.Keyboard.key_m_cache = False
            else:
                Cache.Temp.Keyboard.key_m_cache = True

            if keyboard("n"):
                if Cache.Temp.Keyboard.key_n_cache:
                    text += "N"
                    Cache.Temp.Keyboard.key_n_cache = False
            else:
                Cache.Temp.Keyboard.key_n_cache = True

            if keyboard("o"):
                if Cache.Temp.Keyboard.key_o_cache:
                    text += "O"
                    Cache.Temp.Keyboard.key_o_cache = False
            else:
                Cache.Temp.Keyboard.key_o_cache = True

            if keyboard("p"):
                if Cache.Temp.Keyboard.key_p_cache:
                    text += "P"
                    Cache.Temp.Keyboard.key_p_cache = False
            else:
                Cache.Temp.Keyboard.key_p_cache = True

            if keyboard("q"):
                if Cache.Temp.Keyboard.key_q_cache:
                    text += "Q"
                    Cache.Temp.Keyboard.key_q_cache = False
            else:
                Cache.Temp.Keyboard.key_q_cache = True

            if keyboard("r"):
                if Cache.Temp.Keyboard.key_r_cache:
                    text += "R"
                    Cache.Temp.Keyboard.key_r_cache = False
            else:
                Cache.Temp.Keyboard.key_r_cache = True

            if keyboard("s"):
                if Cache.Temp.Keyboard.key_s_cache:
                    text += "S"
                    Cache.Temp.Keyboard.key_s_cache = False
            else:
                Cache.Temp.Keyboard.key_s_cache = True

            if keyboard("t"):
                if Cache.Temp.Keyboard.key_t_cache:
                    text += "T"
                    Cache.Temp.Keyboard.key_t_cache = False
            else:
                Cache.Temp.Keyboard.key_t_cache = True

            if keyboard("u"):
                if Cache.Temp.Keyboard.key_u_cache:
                    text += "U"
                    Cache.Temp.Keyboard.key_u_cache = False
            else:
                Cache.Temp.Keyboard.key_u_cache = True

            if keyboard("v"):
                if Cache.Temp.Keyboard.key_v_cache:
                    text += "V"
                    Cache.Temp.Keyboard.key_v_cache = False
            else:
                Cache.Temp.Keyboard.key_v_cache = True

            if keyboard("w"):
                if Cache.Temp.Keyboard.key_w_cache:
                    text += "W"
                    Cache.Temp.Keyboard.key_w_cache = False
            else:
                Cache.Temp.Keyboard.key_w_cache = True

            if keyboard("x"):
                if Cache.Temp.Keyboard.key_x_cache:
                    text += "X"
                    Cache.Temp.Keyboard.key_x_cache = False
            else:
                Cache.Temp.Keyboard.key_x_cache = True

            if keyboard("y"):
                if Cache.Temp.Keyboard.key_y_cache:
                    text += "Y"
                    Cache.Temp.Keyboard.key_y_cache = False
            else:
                Cache.Temp.Keyboard.key_y_cache = True

            if keyboard("z"):
                if Cache.Temp.Keyboard.key_z_cache:
                    text += "Z"
                    Cache.Temp.Keyboard.key_z_cache = False
            else:
                Cache.Temp.Keyboard.key_z_cache = True

        if keyboard("a"):
            if Cache.Temp.Keyboard.key_a_cache:
                text += "a"
                Cache.Temp.Keyboard.key_a_cache = False
        else:
            Cache.Temp.Keyboard.key_a_cache = True

        if keyboard("b"):
            if Cache.Temp.Keyboard.key_b_cache:
                text += "b"
                Cache.Temp.Keyboard.key_b_cache = False
        else:
            Cache.Temp.Keyboard.key_b_cache = True

        if keyboard("c"):
            if Cache.Temp.Keyboard.key_c_cache:
                text += "c"
                Cache.Temp.Keyboard.key_c_cache = False
        else:
            Cache.Temp.Keyboard.key_c_cache = True

        if keyboard("d"):
            if Cache.Temp.Keyboard.key_d_cache:
                text += "d"
                Cache.Temp.Keyboard.key_d_cache = False
        else:
            Cache.Temp.Keyboard.key_d_cache = True

        if keyboard("e"):
            if Cache.Temp.Keyboard.key_e_cache:
                text += "e"
                Cache.Temp.Keyboard.key_e_cache = False
        else:
            Cache.Temp.Keyboard.key_e_cache = True

        if keyboard("f"):
            if Cache.Temp.Keyboard.key_f_cache:
                text += "f"
                Cache.Temp.Keyboard.key_f_cache = False
        else:
            Cache.Temp.Keyboard.key_f_cache = True

        if keyboard("g"):
            if Cache.Temp.Keyboard.key_g_cache:
                text += "g"
                Cache.Temp.Keyboard.key_g_cache = False
        else:
            Cache.Temp.Keyboard.key_g_cache = True

        if keyboard("h"):
            if Cache.Temp.Keyboard.key_h_cache:
                text += "h"
                Cache.Temp.Keyboard.key_h_cache = False
        else:
            Cache.Temp.Keyboard.key_h_cache = True

        if keyboard("i"):
            if Cache.Temp.Keyboard.key_i_cache:
                text += "i"
                Cache.Temp.Keyboard.key_i_cache = False
        else:
            Cache.Temp.Keyboard.key_i_cache = True

        if keyboard("j"):
            if Cache.Temp.Keyboard.key_j_cache:
                text += "j"
                Cache.Temp.Keyboard.key_j_cache = False
        else:
            Cache.Temp.Keyboard.key_j_cache = True

        if keyboard("k"):
            if Cache.Temp.Keyboard.key_k_cache:
                text += "k"
                Cache.Temp.Keyboard.key_k_cache = False
        else:
            Cache.Temp.Keyboard.key_k_cache = True

        if keyboard("l"):
            if Cache.Temp.Keyboard.key_l_cache:
                text += "l"
                Cache.Temp.Keyboard.key_l_cache = False
        else:
            Cache.Temp.Keyboard.key_l_cache = True

        if keyboard("m"):
            if Cache.Temp.Keyboard.key_m_cache:
                text += "m"
                Cache.Temp.Keyboard.key_m_cache = False
        else:
            Cache.Temp.Keyboard.key_m_cache = True

        if keyboard("n"):
            if Cache.Temp.Keyboard.key_n_cache:
                text += "n"
                Cache.Temp.Keyboard.key_n_cache = False
        else:
            Cache.Temp.Keyboard.key_n_cache = True

        if keyboard("o"):
            if Cache.Temp.Keyboard.key_o_cache:
                text += "o"
                Cache.Temp.Keyboard.key_o_cache = False
        else:
            Cache.Temp.Keyboard.key_o_cache = True

        if keyboard("p"):
            if Cache.Temp.Keyboard.key_p_cache:
                text += "p"
                Cache.Temp.Keyboard.key_p_cache = False
        else:
            Cache.Temp.Keyboard.key_p_cache = True

        if keyboard("q"):
            if Cache.Temp.Keyboard.key_q_cache:
                text += "q"
                Cache.Temp.Keyboard.key_q_cache = False
        else:
            Cache.Temp.Keyboard.key_q_cache = True

        if keyboard("r"):
            if Cache.Temp.Keyboard.key_r_cache:
                text += "r"
                Cache.Temp.Keyboard.key_r_cache = False
        else:
            Cache.Temp.Keyboard.key_r_cache = True

        if keyboard("s"):
            if Cache.Temp.Keyboard.key_s_cache:
                text += "s"
                Cache.Temp.Keyboard.key_s_cache = False
        else:
            Cache.Temp.Keyboard.key_s_cache = True

        if keyboard("t"):
            if Cache.Temp.Keyboard.key_t_cache:
                text += "t"
                Cache.Temp.Keyboard.key_t_cache = False
        else:
            Cache.Temp.Keyboard.key_t_cache = True

        if keyboard("u"):
            if Cache.Temp.Keyboard.key_u_cache:
                text += "u"
                Cache.Temp.Keyboard.key_u_cache = False
        else:
            Cache.Temp.Keyboard.key_u_cache = True

        if keyboard("v"):
            if Cache.Temp.Keyboard.key_v_cache:
                text += "v"
                Cache.Temp.Keyboard.key_v_cache = False
        else:
            Cache.Temp.Keyboard.key_v_cache = True

        if keyboard("w"):
            if Cache.Temp.Keyboard.key_w_cache:
                text += "w"
                Cache.Temp.Keyboard.key_w_cache = False
        else:
            Cache.Temp.Keyboard.key_w_cache = True

        if keyboard("x"):
            if Cache.Temp.Keyboard.key_x_cache:
                text += "x"
                Cache.Temp.Keyboard.key_x_cache = False
        else:
            Cache.Temp.Keyboard.key_x_cache = True

        if keyboard("y"):
            if Cache.Temp.Keyboard.key_y_cache:
                text += "y"
                Cache.Temp.Keyboard.key_y_cache = False
        else:
            Cache.Temp.Keyboard.key_y_cache = True

        if keyboard("z"):
            if Cache.Temp.Keyboard.key_z_cache:
                text += "z"
                Cache.Temp.Keyboard.key_z_cache = False
        else:
            Cache.Temp.Keyboard.key_z_cache = True



        if keyboard("space"):
            if Cache.Temp.Keyboard.key_specebar_cache:
                text += " "
                Cache.Temp.Keyboard.key_specebar_cache = False
        else:
            Cache.Temp.Keyboard.key_specebar_cache = True

    if set_text[1]:
        if keyboard("1"):
            if Cache.Temp.Keyboard.key_1_cache:
                text += "1"
                Cache.Temp.Keyboard.key_1_cache = False
        else:
            Cache.Temp.Keyboard.key_1_cache = True

        if keyboard("2"):
            if Cache.Temp.Keyboard.key_2_cache:
                text += "2"
                Cache.Temp.Keyboard.key_2_cache = False
        else:
            Cache.Temp.Keyboard.key_2_cache = True

        if keyboard("3"):
            if Cache.Temp.Keyboard.key_3_cache:
                text += "3"
                Cache.Temp.Keyboard.key_3_cache = False
        else:
            Cache.Temp.Keyboard.key_3_cache = True

        if keyboard("4"):
            if Cache.Temp.Keyboard.key_4_cache:
                text += "4"
                Cache.Temp.Keyboard.key_4_cache = False
        else:
            Cache.Temp.Keyboard.key_4_cache = True

        if keyboard("5"):
            if Cache.Temp.Keyboard.key_5_cache:
                text += "5"
                Cache.Temp.Keyboard.key_5_cache = False
        else:
            Cache.Temp.Keyboard.key_5_cache = True

        if keyboard("6"):
            if Cache.Temp.Keyboard.key_6_cache:
                text += "6"
                Cache.Temp.Keyboard.key_6_cache = False
        else:
            Cache.Temp.Keyboard.key_6_cache = True

        if keyboard("7"):
            if Cache.Temp.Keyboard.key_7_cache:
                text += "7"
                Cache.Temp.Keyboard.key_7_cache = False
        else:
            Cache.Temp.Keyboard.key_7_cache = True

        if keyboard("8"):
            if Cache.Temp.Keyboard.key_8_cache:
                text += "8"
                Cache.Temp.Keyboard.key_8_cache = False
        else:
            Cache.Temp.Keyboard.key_8_cache = True

        if keyboard("9"):
            if Cache.Temp.Keyboard.key_9_cache:
                text += "9"
                Cache.Temp.Keyboard.key_9_cache = False
        else:
            Cache.Temp.Keyboard.key_9_cache = True

        if keyboard("0"):
            if Cache.Temp.Keyboard.key_0_cache:
                text += "0"
                Cache.Temp.Keyboard.key_0_cache = False
        else:
            Cache.Temp.Keyboard.key_0_cache = True

        if keyboard("period"):
            if Cache.Temp.Keyboard.key_period_cache:
                text += "."
                Cache.Temp.Keyboard.key_period_cache = False
        else:
            Cache.Temp.Keyboard.key_period_cache = True

    if keyboard("back"):
        if Cache.Temp.Keyboard.key_backspace_cache:
            text = text[:-1]
            Cache.Temp.Keyboard.key_backspace_cache = False
    else:
        Cache.Temp.Keyboard.key_backspace_cache = True

    return str(text)
