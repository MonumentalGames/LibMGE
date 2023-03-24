import pygame
from PIL import Image as PIL_Image

class Cache:

    class Temp:
        class Screen:
            class IMG:
                def __init__(self, img=None):
                    if img is not None:
                        self.image = img
                        image_size = self.image.get_size()

                        #res = 480 / image_size[1]
                        #image_size = (int(res * image_size[0]), int(res * image_size[1]))

                        raw_str = pygame.image.tostring(pygame.transform.scale(self.image, image_size), "RGB", False)
                        self.image = PIL_Image.frombytes("RGB", image_size, raw_str)
                        self.size = self.image.size
                    else:
                        self.image = PIL_Image.new("RGB", (32, 32), color=(0, 0, 0))
                        self.size = self.image.size

                def set_img(self, img=None):
                    if img is not None:
                        self.image = img
                        image_size = self.image.get_size()

                        #res = 480 / image_size[1]
                        #image_size = (int(res * image_size[0]), int(res * image_size[1]))

                        raw_str = pygame.image.tostring(pygame.transform.scale(self.image, image_size), "RGB", False)
                        self.image = PIL_Image.frombytes("RGB", image_size, raw_str)
                        self.size = self.image.size
                    else:
                        self.image = PIL_Image.new("RGB", (32, 32), color=(0, 0, 0))
                        self.size = self.image.size
            img = IMG()

        Keyboard = {
            "key_all_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_esc_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_specebar_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_backspace_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_period_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_return_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_tab_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_shift_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_ctrl_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_alt_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_1_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_2_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_3_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_4_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_5_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_6_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_7_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_8_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_9_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_0_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_kp1_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp2_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp3_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp4_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp5_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp6_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp7_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp8_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp9_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_kp0_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_a_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_b_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_c_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_d_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_e_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_g_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_h_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_i_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_j_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_k_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_l_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_m_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_n_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_o_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_p_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_q_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_r_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_s_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_t_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_u_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_v_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_w_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_x_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_y_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_z_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_up_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_down_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_left_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_right_cache": {"press": True, "time": {"press": 0, "loop": 0}},

            "key_f1_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f2_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f3_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f4_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f5_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f6_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f7_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f8_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f9_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f10_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f11_cache": {"press": True, "time": {"press": 0, "loop": 0}},
            "key_f12_cache": {"press": True, "time": {"press": 0, "loop": 0}}
        }

        Button = {"button_active": False}

        Mouse = {"button_cache": [False, False, False, False, False]}
