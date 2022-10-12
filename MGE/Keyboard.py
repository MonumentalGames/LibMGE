import pygame

Key_All = "all"

Key_A = "a"
Key_B = "b"
Key_C = "c"
Key_D = "d"
Key_E = "e"
Key_F = "f"
Key_G = "g"
Key_H = "h"
Key_I = "i"
Key_J = "j"
Key_K = "k"
Key_L = "l"
Key_M = "m"
Key_N = "n"
Key_O = "o"
Key_P = "p"
Key_Q = "q"
Key_R = "r"
Key_S = "s"
Key_T = "t"
Key_U = "u"
Key_V = "v"
Key_W = "w"
Key_X = "x"
Key_Y = "y"
Key_Z = "z"

Key_1 = "1"
Key_2 = "2"
Key_3 = "3"
Key_4 = "4"
Key_5 = "5"
Key_6 = "6"
Key_7 = "7"
Key_8 = "8"
Key_9 = "9"
Key_0 = "0"

Key_NUM_1 = "NUM1"
Key_NUM_2 = "NUM2"
Key_NUM_3 = "NUM3"
Key_NUM_4 = "NUM4"
Key_NUM_5 = "NUM5"
Key_NUM_6 = "NUM6"
Key_NUM_7 = "NUM7"
Key_NUM_8 = "NUM8"
Key_NUM_9 = "NUM9"
Key_NUM_0 = "NUM0"

Key_F1 = "f1"
Key_F2 = "f2"
Key_F3 = "f3"
Key_F4 = "f4"
Key_F5 = "f5"
Key_F6 = "f6"
Key_F7 = "f7"
Key_F8 = "f8"
Key_F9 = "f9"
Key_F10 = "f10"
Key_F11 = "f11"
Key_F12 = "f12"

Key_ESCAPE = "esc"
Key_BACKSPACE = "back"

def keyboard(key):
    key = str(key).lower()
    event_key = pygame.key.get_pressed()

    if key == "all":
        for cache_key in event_key:
            if cache_key:
                return True

    if key == '1':
        if event_key[pygame.K_1]:
            return True
    if key == '2':
        if event_key[pygame.K_2]:
            return True
    if key == '3':
        if event_key[pygame.K_3]:
            return True
    if key == '4':
        if event_key[pygame.K_4]:
            return True
    if key == '5':
        if event_key[pygame.K_5]:
            return True
    if key == '6':
        if event_key[pygame.K_6]:
            return True
    if key == '7':
        if event_key[pygame.K_7]:
            return True
    if key == '8':
        if event_key[pygame.K_8]:
            return True
    if key == '9':
        if event_key[pygame.K_9]:
            return True
    if key == '0':
        if event_key[pygame.K_0]:
            return True

    if key == 'a':
        if event_key[pygame.K_a]:
            return True
    if key == 'b':
        if event_key[pygame.K_b]:
            return True
    if key == 'c':
        if event_key[pygame.K_c]:
            return True
    if key == 'd':
        if event_key[pygame.K_d]:
            return True
    if key == 'e':
        if event_key[pygame.K_e]:
            return True
    if key == 'f':
        if event_key[pygame.K_f]:
            return True
    if key == 'g':
        if event_key[pygame.K_g]:
            return True
    if key == 'h':
        if event_key[pygame.K_h]:
            return True
    if key == 'i':
        if event_key[pygame.K_i]:
            return True
    if key == 'j':
        if event_key[pygame.K_j]:
            return True
    if key == 'k':
        if event_key[pygame.K_k]:
            return True
    if key == 'l':
        if event_key[pygame.K_l]:
            return True
    if key == 'm':
        if event_key[pygame.K_m]:
            return True
    if key == 'n':
        if event_key[pygame.K_n]:
            return True
    if key == 'o':
        if event_key[pygame.K_o]:
            return True
    if key == 'p':
        if event_key[pygame.K_p]:
            return True
    if key == 'q':
        if event_key[pygame.K_q]:
            return True
    if key == 'r':
        if event_key[pygame.K_r]:
            return True
    if key == 's':
        if event_key[pygame.K_s]:
            return True
    if key == 't':
        if event_key[pygame.K_t]:
            return True
    if key == 'u':
        if event_key[pygame.K_u]:
            return True
    if key == 'v':
        if event_key[pygame.K_v]:
            return True
    if key == 'w':
        if event_key[pygame.K_w]:
            return True
    if key == 'x':
        if event_key[pygame.K_x]:
            return True
    if key == 'y':
        if event_key[pygame.K_y]:
            return True
    if key == 'z':
        if event_key[pygame.K_z]:
            return True

    if key == "esc":
        if event_key[pygame.K_ESCAPE]:
            return True

    if key == 'back':
        if event_key[pygame.K_BACKSPACE]:
            return True

    if key == 'up':
        if event_key[pygame.K_UP]:
            return True
    if key == 'down':
        if event_key[pygame.K_DOWN]:
            return True
    if key == 'left':
        if event_key[pygame.K_LEFT]:
            return True
    if key == 'right':
        if event_key[pygame.K_RIGHT]:
            return True

    if key == 'space':
        if event_key[pygame.K_SPACE]:
            return True

    if key == 'return':
        if event_key[pygame.K_RETURN]:
            return True

    if key == "shift":
        if event_key[pygame.K_LSHIFT] or event_key[pygame.K_RSHIFT]:
            return True
    if key == "left_shift":
        if event_key[pygame.K_LSHIFT]:
            return True
    if key == "right_shift":
        if event_key[pygame.K_RSHIFT]:
            return True

    if key == "ctrl":
        if event_key[pygame.K_LCTRL] or event_key[pygame.K_RCTRL]:
            return True
    if key == "left_ctrl":
        if event_key[pygame.K_LCTRL]:
            return True
    if key == "right_ctrl":
        if event_key[pygame.K_RCTRL]:
            return True

    if key == "alt":
        if event_key[pygame.K_LALT] or event_key[pygame.K_RALT]:
            return True
    if key == "left_alt":
        if event_key[pygame.K_LALT]:
            return True
    if key == "right_alt":
        if event_key[pygame.K_RALT]:
            return True

    if key == 'f1':
        if event_key[pygame.K_F1]:
            return True
    if key == 'f2':
        if event_key[pygame.K_F2]:
            return True
    if key == 'f3':
        if event_key[pygame.K_F3]:
            return True
    if key == 'f4':
        if event_key[pygame.K_F4]:
            return True
    if key == 'f5':
        if event_key[pygame.K_F5]:
            return True
    if key == 'f6':
        if event_key[pygame.K_F6]:
            return True
    if key == 'f7':
        if event_key[pygame.K_F7]:
            return True
    if key == 'f8':
        if event_key[pygame.K_F8]:
            return True
    if key == 'f9':
        if event_key[pygame.K_F9]:
            return True
    if key == 'f10':
        if event_key[pygame.K_F10]:
            return True
    if key == 'f11':
        if event_key[pygame.K_F11]:
            return True
    if key == 'f12':
        if event_key[pygame.K_F12]:
            return True
