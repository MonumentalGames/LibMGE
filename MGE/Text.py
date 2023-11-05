import threading
import os

from .Common import _temp, _calculate_object2d
from .Constants import *
from .Camera import Camera
from .Keyboard import keyboard, KeyboardText, KeyboardClick
from .Time import Time, fps_to_time
from .Platform import Platform
from .Color import Color
from .Mouse import GetMousePosition, MouseButton
from ._sdl import sdl2, sdlttf

if Platform.system == "Windows":
    _DefaultFontDirectory = "C:/Windows/Fonts"
    _DefaultFont = "verdana"
else:
    _DefaultFontDirectory = ""
    _DefaultFont = "verdana"

__all__ = ["ObjectText", "ObjectTextBox",
           "GetClipboardText", "SetClipboardText"]

def GetClipboardText() -> str:
    return sdl2.SDL_GetClipboardText().decode()

def SetClipboardText(text: str):
    sdl2.SDL_SetClipboardText(text.encode())

class ObjectText:
    def __init__(self, location=(0, 0), size: int = 20, rotation: int = 0, text: str = "", font=_DefaultFont):
        self._location = list(location)
        self._size = size
        self._rotation = rotation
        self._rotation %= 360

        self._max_width = 0

        self.pivot = Pivot2D.TopLeftSide

        if os.path.exists(font):
            self._font = font
        else:
            self._font = f"{_DefaultFontDirectory}/{font}.ttf" if os.path.exists(f"{_DefaultFontDirectory}/{font}.ttf") else f"{_DefaultFontDirectory}/{_DefaultFont}.ttf"

        self._color = Color((255, 255, 255, 255))
        self._background_color = Color((0, 0, 0, 0))
        self._text = text

        self._threading = threading.Thread()
        self.render_time = Time(fps_to_time(60))

        self.text_render_cache = False

        self._cursor = 11

        self._text_render_type = 0

        self._text_surface = None
        self._text_surface_th = None
        self._text_font = sdlttf.TTF_OpenFont(self._font, self._size)

        #sdlttf.TTF_SetFontDirection(self.text_render_font, 3)

        self._text_surface_size = list(sdlttf.TTF_SizeUTF8(self._text_font, self._text.encode()))

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        if self._font != font:
            self._font = font
            if self._text_font is not None:
                sdlttf.TTF_CloseFont(self._text_font)
            self._text_font = sdlttf.TTF_OpenFont(self._font, self._size)
            self.text_render_cache = False

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, color: Color):
        if isinstance(color, Color):
            if self._color != color:
                self._color = color
                self.text_render_cache = False
        else:
            if self._color.RGB != color and self._color.RGBA != color:
                self._color = Color(color)
                self.text_render_cache = False

    @property
    def backgroundColor(self) -> Color:
        return self._background_color

    @backgroundColor.setter
    def backgroundColor(self, color: Color):
        if isinstance(color, Color):
            if self._background_color != color:
                self._background_color = color
                self.text_render_cache = False
        else:
            if self._background_color.RGB != color and self._background_color.RGBA != color:
                self._background_color = Color(color)
                self.text_render_cache = False

    @property
    def style(self):
        return sdlttf.TTF_GetFontStyle(self._text_font)

    @style.setter
    def style(self, style):
        sdlttf.TTF_SetFontStyle(self._text_font, style)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        if self._text != text:
            self._text = text
            self.text_render_cache = False

    @property
    def location(self) -> list[int, int]:
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int):
        if self._size != size:
            self._size = size
            sdlttf.TTF_SetFontSize(self._text_font, self._size)
            self.text_render_cache = False

    @property
    def surfaceSize(self) -> list[int, int]:
        if not self._threading.is_alive() and not self.text_render_cache:
            return sdlttf.TTF_SizeUTF8(self._text_font, self._text.encode())
        return self._text_surface_size

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: int | float):
        self._rotation = round(rotation, 4)
        self._rotation %= 360

    @property
    def maxWidth(self):
        return self._max_width

    @maxWidth.setter
    def maxWidth(self, max_width: int):
        self._max_width = max_width

    @property
    def _surface(self):
        return self._text_surface_th if self._threading.is_alive() else self._text_surface

    @_surface.setter
    def _surface(self, surf):
        if isinstance(self._text_surface, sdl2.SDL_Surface):
            sdl2.SDL_FreeSurface(self._text_surface)
        self._text_surface = surf

    def _threading_render(self):
        if not self._threading.is_alive():
            if self._text_surface is not None:
                if self._text_surface_th is not None:
                    sdl2.SDL_FreeSurface(self._text_surface_th)
                self._text_surface_th = sdl2.SDL_ConvertSurface(self._text_surface, self._text_surface.format, 0).contents
            self._threading = threading.Thread(target=self._render)
            self._threading.daemon = True
            self._threading.start()

    def _render(self):
        _text = self._text.replace("\n\n", "\n \n")
        _text = _text.replace("\r\n", "\n").replace("\r", "\n")
        if self._background_color._a > 0:
            self._surface = sdlttf.TTF_RenderUTF8_Shaded_Wrapped(self._text_font, _text.encode(), self._color.SDLColor, self._background_color.SDLColor, self._max_width).contents
        else:
            self._surface = sdlttf.TTF_RenderUTF8_Blended_Wrapped(self._text_font, _text.encode(), self._color.SDLColor, self._max_width).contents
        self._text_surface_size = [self._text_surface.w, self._text_surface.h]
        self.text_render_cache = True

    def render(self):
        if not self.text_render_cache and not self._threading.is_alive():
            if self.render_time.tick(True):
                if self._text_render_type == 0:
                    self._render()
                elif self._text_render_type == 1:
                    self._threading_render()

    def draw_object(self, window, camera: Camera = None, render: bool = True):
        if self._text:
            if window.__Window_Active__:
                if self not in window.draw_objects:
                    window.draw_objects.append(self)
                    _render, cache_location, cache_size = _calculate_object2d(self._location, self._text_surface_size, 0, [1, 1], window, camera, self.pivot)
                    if _render:
                        if render:
                            self.render()
                        window.blit(self._surface, cache_location, None, self._rotation)

    def hover(self, window, camera: Camera = None) -> bool:
        _render, cache_location, cache_size = _calculate_object2d(self._location, self._text_surface_size, 0, [1, 1], window, camera, self.pivot)
        mouse_lok = GetMousePosition()
        if _render and (cache_location[0] < mouse_lok[0] < cache_location[0] + cache_size[0] and cache_location[1] < mouse_lok[1] < cache_location[1] + cache_size[1]):
            _temp.MouseCursor = self._cursor
            return True

class ObjectTextBox:
    def __init__(self, location=(0, 0), size: int = 20, rotation: int = 0, default_text: str = "", text: str = "", font=_DefaultFont):
        self._default_text = default_text
        self._text = text
        self._cache_text = [self._text]
        self._time_text = Time(0.25)

        self.loc = 0
        self.selected = [0, 0]

        self._limit_size = None

        self._p_start_timer = Time(1)
        self._p_timer = Time(0.5)

        self.type = "all"

        self._copy_and_paste = True

        self._ObjectText = ObjectText(location=location, size=size, rotation=rotation, text=self._text, font=font)
        self._ObjectText._cursor = 1

        self._State = True

        self.tt = True

    def input_text(self, text):
        if text is not None:
            if self.selected[0] != self.selected[1]:
                result = ''
                for i, letra in enumerate(self._text):
                    if not self.selected_box[0] <= i < self.selected_box[1]:
                        result += letra
                result2 = ''
                for i, letra in enumerate(result):
                    if i == self.selected_box[0] if self.selected_box[0] <= len(self._text) - 1 else self.selected_box[0] <= len(self._text) - 1:
                        result2 += text
                    result2 += letra
                self._text = result2

            elif self.loc != len(self._text):
                result = ''
                for i, letra in enumerate(self._text):
                    if i == self.loc if self.loc <= len(self._text) - 1 else self.loc <= len(self._text) - 1:
                        result += text
                    result += letra
                self._text = result

            else:
                self._text += text

            self.loc = self.selected_box[0] + len(text) if self.selected[0] != self.selected[1] else self.loc + len(text)
            self.selected[1] = self.selected[0] = self.loc

    @property
    def selected_box(self) -> list[int, int]:
        if self.selected[0] != self.selected[1]:
            if self.selected[0] > self.selected[1]:
                return [self.selected[1], self.selected[0]]
            return self.selected
        return [self.loc, self.loc]

    @property
    def selected_text(self):
        result = ""
        for i, letra in enumerate(self._text):
            if self.selected_box[0] <= i < self.selected_box[1]:
                result += letra
        return result

    def update(self, window, camera: Camera = None):

        def mouse_text():
            self._p_start_timer.restart()

            def lens(li, ind):
                return sum(len(li[num]) for num in range(ind))

            def text(texts, loc):
                return texts[self._text[:loc].count("\n")][:loc - lens(texts, self._text[:loc].count("\n")) - self._text[:loc].count("\n")]

            _texts = self._text.split("\n")
            loc = GetMousePosition()[0] - self._ObjectText.location[0], GetMousePosition()[1] - self._ObjectText.location[1]
            posicao_mais_proxima = None
            menor_diferenca = float('inf')

            for let in range(len(_texts[0]) + 1):
                q_size = sdlttf.TTF_SizeUTF8(self._ObjectText._text_font, text(_texts, let).encode())
                diferenca = abs(loc[0] - q_size[0])
                if diferenca < menor_diferenca:
                    menor_diferenca = diferenca
                    posicao_mais_proxima = let
                else:
                    break

            self.loc = posicao_mais_proxima

        if self._State:
            if len(self._cache_text) >= 25:
                self._cache_text = self._cache_text[1:]

            if keyboard(KeyboardButton.KeyboardButton_Ctrl, True):
                if self._copy_and_paste:
                    if keyboard(KeyboardButton.KeyboardButton_C):
                        _text = self.selected_text
                        SetClipboardText(_text if _text else self._text)
                    if keyboard(KeyboardButton.KeyboardButton_V):
                        self.input_text(GetClipboardText())
                    if keyboard(KeyboardButton.KeyboardButton_X):
                        _text = self.selected_text
                        SetClipboardText(_text if _text else self._text)
                        self.selected = self.selected if _text else [0, len(self._text)]
                        self.input_text("")

                if keyboard(KeyboardButton.KeyboardButton_Z):
                    if len(self._cache_text) > 1:
                        self._text = str(self._cache_text[len(self._cache_text) - 2])
                        self._cache_text = self._cache_text[:-1]

            if keyboard(KeyboardButton.KeyboardButton_Shift):
                self.selected[0] = self.loc
            if keyboard(KeyboardButton.KeyboardButton_Shift, True):
                self.selected[1] = self.loc

            self.input_text(KeyboardText())

            click = KeyboardClick()
            if click is not None:
                self._p_start_timer.restart()
                if click == KeyboardButton.KeyboardButton_Back:
                    if self.selected[0] != self.selected[1]:
                        result = ''
                        for i, letra in enumerate(self._text):
                            if not self.selected_box[0] <= i < self.selected_box[1]:
                                result += letra
                        self._text = result
                    elif self.loc != len(self._text):
                        result = ''
                        for i, letra in enumerate(self._text):
                            if i == self.loc if self.loc <= len(self._text) - 1 else self.loc <= len(self._text) - 1:
                                result = result[:-1]
                            result += letra
                        self._text = result
                    else:
                        self._text = self._text[:-1]
                    self.loc = self.selected_box[0] if self.selected[0] != self.selected[1] else self.loc - 1
                    self.selected[1] = self.selected[0]

                elif click == KeyboardButton.KeyboardButton_Return:
                    self.input_text("\n")
                elif click == KeyboardButton.KeyboardButton_Tab:
                    self.input_text("    ")

                elif click == 80:
                    self.loc -= 1
                    if not keyboard(KeyboardButton.KeyboardButton_Shift, True):
                        self.selected[0] = self.selected[1] = self.loc
                elif click == 79:
                    self.loc += 1
                    if not keyboard(KeyboardButton.KeyboardButton_Shift, True):
                        self.selected[0] = self.selected[1] = self.loc

            if self.loc < 0:
                self.loc = 0
            if self.loc > len(self._text):
                self.loc = len(self._text)

            if keyboard(-1, True):
                self._time_text.restart()
            if self._time_text.tick():
                if self._text != self._cache_text[len(self._cache_text) - 1]:
                    self._cache_text.append(self._text)

            if self._ObjectText.hover(window, camera):
                if MouseButton(1):
                    mouse_text()
                    self.selected[0] = self.loc
                    self.tt = True
            else:
                if MouseButton(1):
                    self._State = False

            if MouseButton(1, True) and self.tt:
                mouse_text()
                self.selected[1] = self.loc
            else:
                self.tt = False

            self._ObjectText.text = self._text
        else:
            if self._ObjectText.hover(window, camera):
                if MouseButton(1):
                    self._State = True
                    mouse_text()
                    self.selected[1] = self.selected[0] = self.loc
                    self.tt = True

    def draw_object(self, window, camera: Camera = None, render: bool = True):
        if window.__Window_Active__:
            if self not in window.draw_objects:
                window.draw_objects.append(self)

                _texts = self._text.split("\n")

                def lens(li, ind):
                    return sum(len(li[num]) for num in range(ind))

                def text(texts, loc):
                    return texts[self._text[:loc].count("\n")][:loc - lens(texts, self._text[:loc].count("\n")) - self._text[:loc].count("\n")]

                if self.selected[0] != self.selected[1]:

                    if "\n" in self.selected_text:
                        print(self.selected_text.count("\n"))

                    q_size = sdlttf.TTF_SizeUTF8(self._ObjectText._text_font, text(_texts, self.selected_box[0]).encode())
                    qs_size = sdlttf.TTF_SizeUTF8(self._ObjectText._text_font, self.selected_text.replace("\n", "").encode())

                    loc = [0, q_size[1] * self._text[:self.loc].count("\n")]

                    window.drawSquare([self._ObjectText.location[0] + q_size[0], self._ObjectText.location[1] + loc[1]], qs_size, 0, 0, Color((75, 75, 255, 150)))

                self._ObjectText.draw_object(window, camera, render)

                if self._State:
                    if self._p_timer.tickFlipFlop() or not self._p_start_timer.tick():
                        #print(text(_texts, self.loc))
                        size = sdlttf.TTF_SizeUTF8(self._ObjectText._text_font, text(_texts, self.loc).encode())

                        loc = [0, size[1] * self._text[:self.loc].count("\n")]

                        L_loc_1 = [self._ObjectText.location[0] + size[0] + loc[0], self._ObjectText.location[1] + loc[1] + 1]
                        L_loc_2 = [self._ObjectText.location[0] + size[0] + loc[0], self._ObjectText.location[0] + size[1] + loc[1] - 2]

                        window.drawLine(L_loc_1, L_loc_2, 2, Color((255, 255, 255)))

    def clean_cache(self):
        self._cache_text.clear()
