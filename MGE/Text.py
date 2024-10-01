import os
from threading import Thread

from .Common import _temp, _calculate_object2d
from .Constants import *
from .Camera import Camera
from .Keyboard import keyboard, KeyboardText, KeyboardClick
from .Time import Time, fps_to_time
from .Platform import Platform
from .Color import Color
from .Mouse import GetMousePosition, MouseButton, MouseScroll, object2dSimpleHover
from .Window import Window, InternalWindow
from ._sdl import sdl2, sdlttf, sdlgfx

if Platform.system == "Windows":
    _DefaultFontDirectory = "C:/Windows/Fonts"
    _DefaultFont = "verdana"
else:
    _DefaultFontDirectory = ""
    _DefaultFont = "verdana"

__all__ = ["ObjectText", "ObjectInputTextLine", "ObjectInputTextBox",
           "GetClipboardText", "SetClipboardText"]

def GetClipboardText() -> str: return sdl2.SDL_GetClipboardText()
def SetClipboardText(text: str): sdl2.SDL_SetClipboardText(text)

class _ObjectText:
    def __init__(self, font_size, text, font):
        self._text = text
        self._font_size = font_size

        self._color = Color((255, 255, 255, 255))

        if os.path.exists(font):
            self._font = font
        else:
            self._font = f"{_DefaultFontDirectory}/{font}.ttf" if os.path.exists(f"{_DefaultFontDirectory}/{font}.ttf") else f"{_DefaultFontDirectory}/{_DefaultFont}.ttf"

        self._text_font = sdlttf.TTF_OpenFont(self._font, self._font_size)

        self._text_render_type = 1
        self._threading = Thread()
        self.render_time = Time(fps_to_time(60))

        self._text_surface = None
        self._text_surface_th = None

        self._render_cache = False

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
            self._text_font = sdlttf.TTF_OpenFont(self._font, self._font_size)
            self._render_cache = False

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, color: Color):
        if isinstance(color, Color):
            if self._color != color:
                self._color = color
                self._render_cache = False
        else:
            if self._color.RGB != color and self._color.RGBA != color:
                self._color = Color(color)
                self._render_cache = False

    @property
    def style(self):
        return sdlttf.TTF_GetFontStyle(self._text_font)

    @style.setter
    def style(self, style):
        sdlttf.TTF_SetFontStyle(self._text_font, style)

    @property
    def text(self) -> str:
        return self._text.replace("\n\n", "\n \n").replace("\r\n", "\n").replace("\r", "\n")

    @text.setter
    def text(self, text: str):
        if self._text != text:
            self._text = text
            self._render_cache = False

    @property
    def surfaceSize(self) -> list[int, int]:
        if not self._threading.is_alive() and not self._render_cache:
            return sdlttf.TTF_SizeUTF8(self._text_font, self._text.encode())
        return self._text_surface_size

    @property
    def _surface(self):
        return self._text_surface_th if self._threading.is_alive() else self._text_surface

    @_surface.setter
    def _surface(self, surf):
        if isinstance(self._text_surface, sdl2.SDL_Surface):
            sdl2.SDL_FreeSurface(self._text_surface)
        self._text_surface = surf

    def _multi_threading_render(self):
        if not self._threading.is_alive():
            if self._text_surface is not None:
                if self._text_surface_th is not None:
                    sdl2.SDL_FreeSurface(self._text_surface_th)
                self._text_surface_th = sdl2.SDL_DuplicateSurface(self._text_surface).contents
            self._threading = Thread(target=self._single_threading_render)
            self._threading.daemon = True
            self._threading.start()

    def _single_threading_render(self):
        _text = self.text
        _text = _text if _text else " "
        self._surface = sdlttf.TTF_RenderUTF8_Blended_Wrapped(self._text_font, _text.encode(), self._color.SDLColor, 0).contents
        self._text_surface_size = [self._text_surface.w, self._text_surface.h]
        self._render_cache = True

    def _render(self):
        if not self._render_cache and not self._threading.is_alive():
            if self.render_time.tick(True):
                if self._text_render_type == 0:
                    self._single_threading_render()
                elif self._text_render_type == 1:
                    self._multi_threading_render()

    def _close(self):
        if isinstance(self._text_surface_th, sdl2.SDL_Surface):
            sdl2.SDL_FreeSurface(self._text_surface_th)
        if isinstance(self._text_surface, sdl2.SDL_Surface):
            sdl2.SDL_FreeSurface(self._text_surface)
        sdlttf.TTF_CloseFont(self._text_font)

class ObjectText(_ObjectText):
    def __init__(self, location=(0, 0), rotation: int = 0, font_size: int = 20, text: str = "", font=_DefaultFont):
        super().__init__(font_size, text, font)
        self._location = list(location)
        self._rotation = rotation
        self._rotation %= 360

        self._pivot = Pivot2D.TopLeftSide

        self._background_color = Color((0, 0, 0, 0))

        self.text_render_cache = False

        self._cursor = 11

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

    def realLocation(self, window, camera: Camera = None):
        _render, cache_location, cache_size = _calculate_object2d(self._location, self._text_surface_size, 0, [1, 1], window, camera, self._pivot)
        return cache_location

    @property
    def location(self) -> list[int, int]:
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def size(self) -> int:
        return self._font_size

    @size.setter
    def size(self, size: int):
        if self._font_size != size:
            self._font_size = size
            sdlttf.TTF_SetFontSize(self._text_font, self._font_size)
            self.text_render_cache = False

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: int | float):
        self._rotation = round(rotation, 4)
        self._rotation %= 360

    def render(self):
        self._render()

    def close(self):
        self._close()

    def drawObject(self, window, camera: Camera = None, render: bool = True):
        if self._text:
            if window.__WindowActive__:
                if self not in window.drawnObjects:
                    window.drawnObjects.append(self)
                    _render, cache_location, cache_size = _calculate_object2d(self._location, self._text_surface_size, 0, [1, 1], window, camera, self._pivot)
                    if _render:
                        if render:
                            self._render()
                        window.blit(self._surface, cache_location, None, self._rotation)

    def hover(self, window: Window | InternalWindow, camera: Camera = None) -> bool:
        return object2dSimpleHover(window, camera, self._location, self._text_surface_size, (1, 1), self._pivot)

class _ObjectInputText(_ObjectText):
    def __init__(self, font_size, text, font):
        super().__init__(font_size, text, font)
        self._location = [0, 0]
        self._position = 0
        self.selected = [0, 0]

        self._cache_text = [self._text]

        self.scroll = [0, 0]

        self._p_start_timer = Time(1)
        self._p_timer = Time(0.5)

    def _inputText(self, text):
        if text is not None:
            if self.selected[0] != self.selected[1]:
                result = ''
                for i, letra in enumerate(self._text):
                    if not self.selectedBox[0] <= i < self.selectedBox[1]:
                        result += letra
                result2 = ''
                for i, letra in enumerate(result):
                    if i == self.selectedBox[0] if self.selectedBox[0] <= len(self._text) - 1 else self.selectedBox[0] <= len(self._text) - 1:
                        result2 += text
                    result2 += letra
                if self._text != result2:
                    self._render_cache = False
                    self._text = result2

            elif self._position != len(self._text):
                result = ''
                for i, letra in enumerate(self._text):
                    if i == self._position if self._position <= len(self._text) - 1 else self._position <= len(self._text) - 1:
                        result += text
                    result += letra
                if self._text != result:
                    self._render_cache = False
                    self._text = result

            else:
                self._render_cache = False
                self._text += text

            self.selected[1] = self.selected[0] = self._position = self.selectedBox[0] + len(text) if self.selected[0] != self.selected[1] else self._position + len(text)
            return True
        return False

    def _textMousePosition(self, window):
        self._p_start_timer.restart()
        self._p_timer.flipflop = True
        _texts = self._text.split("\n")
        _mouse_position = GetMousePosition()
        _mouse_position = (_mouse_position[0] - self._location[0] + 1 - self.scroll[0], _mouse_position[1] - self._location[1] - self.scroll[1])

        if isinstance(window, InternalWindow):
            _mouse_position = _mouse_position[0] - window.location[0], _mouse_position[1] - window.location[1]

        if _mouse_position[1] < 0:
            _line = 1
        else:
            _line_size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[0].encode())[1]
            _line = min(int(_mouse_position[1] / _line_size) + 1, len(_texts))

        _less_diff = float('inf')
        _position = 0

        for let in range(len(_texts[_line - 1]) + 1):
            _text_size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[_line - 1][:let].encode())
            _diff = abs(_mouse_position[0] - _text_size[0])
            if _diff < _less_diff:
                _less_diff = _diff
                _position = let
            else:
                break

        if _line > 1:
            _position += sum(len(_texts[p]) + 1 for p in range(_line - 1))

        self._position = _position
        return self._position

    @property
    def selectedBox(self) -> list[int, int]:
        if self.selected[0] != self.selected[1]:
            if self.selected[0] > self.selected[1]:
                return [self.selected[1], self.selected[0]]
            return self.selected
        return [self._position, self._position]

    @property
    def selectedText(self):
        result = ""
        for i, letra in enumerate(self._text):
            if self.selectedBox[0] <= i < self.selectedBox[1]:
                result += letra
        return result

    def clean_cache(self):
        self._cache_text.clear()

class ObjectInputTextLine(_ObjectInputText):
    def __init__(self, location=(0, 0), size=(200, 200), rotation: int = 0, font_size: int = 20, background_text: str = "", text: str = "", font=_DefaultFont):
        super().__init__(font_size, text, font)
        self._location = list(location)
        self._size = list(size)
        self._rotation = rotation
        self._rotation %= 360

        self._pivot = Pivot2D.TopLeftSide

        self._background_color = Color((0, 0, 0, 0))

        self._cursor = 1

        self._surface_object = sdl2.SDL_CreateRGBSurface(0, self._size[0]+2, sdlttf.TTF_SizeUTF8(self._text_font, b" ")[1], 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000).contents
        self._surface_object_tx = None
        self._surface_object_rd = sdl2.SDL_CreateSoftwareRenderer(self._surface_object)

        self._text_surface_tx = None

        self._background_text = background_text
        self._time_text = Time(0.25)

        self._copy_and_paste = True

        self._State = False

        self._text_render_type = 0

        self.scroll = [0, 0]

        self._tt = True

    @property
    def column(self):
        return self._position

    def update(self, window, camera: Camera = None):

        if self.hover(window, camera):
            _temp.MouseCursor = self._cursor
            if not self._State and MouseButton(1):
                self._State = self._tt = True
                self.selected[1] = self.selected[0] = self._textMousePosition(window)
        if self._State:
            _texts = self.text

            if len(self._cache_text) >= 25:
                self._cache_text = self._cache_text[1:]

            if keyboard(KeyboardButton.Ctrl, True):
                if self._copy_and_paste:
                    if keyboard(KeyboardButton.KeyC):
                        _text = self.selectedText
                        SetClipboardText(_text if _text else self.text)
                    if keyboard(KeyboardButton.KeyV):
                        self._inputText(GetClipboardText())
                    if keyboard(KeyboardButton.KeyX):
                        _text = self.selectedText
                        SetClipboardText(_text if _text else self.text)
                        self.selected = self.selected if _text else [0, len(self.text)]
                        self._inputText("")

                if keyboard(KeyboardButton.KeyZ):
                    if len(self._cache_text) > 1:
                        self._text = str(self._cache_text[len(self._cache_text) - 2])
                        self._cache_text = self._cache_text[:-1]

            if keyboard(KeyboardButton.Shift):
                self.selected[0] = self._position
            if keyboard(KeyboardButton.Shift, True):
                self.selected[1] = self._position

            self._inputText(KeyboardText())

            click = KeyboardClick()
            if click is not None:
                self._p_start_timer.restart()
                self._p_timer.flipflop = True
                if click == KeyboardButton.Back:
                    if self.selected[0] != self.selected[1]:
                        self._inputText("")
                    else:
                        if self._position != len(self.text):
                            result = ''
                            for i, letra in enumerate(self.text):
                                if i == self._position if self._position <= len(self.text) - 1 else self._position <= len(self.text) - 1:
                                    result = result[:-1]
                                result += letra
                            self.text = result
                        else:
                            self.text = self.text[:-1]
                        self._position -= 1
                        self._render_cache = False

                elif click == KeyboardButton.Tab:
                    self._inputText("   ")

                # motion
                elif click in (KeyboardButton.Left, KeyboardButton.Right):
                    if click == KeyboardButton.Left:
                        self._position -= 1
                    elif click == KeyboardButton.Right:
                        self._position += 1
                    if not keyboard(KeyboardButton.Shift, True):
                        self.selected[0] = self.selected[1] = self._position

                elif click in (KeyboardButton.Up, KeyboardButton.Down):
                    if not keyboard(KeyboardButton.Shift, True):
                        self.selected[0] = self.selected[1] = self._position

            if self._position < 0:
                self._position = 0
            if self._position > len(self._text):
                self._position = len(self._text)

            if keyboard(-1, True):
                self._time_text.restart()
            if self._time_text.tick():
                if self._text != self._cache_text[len(self._cache_text) - 1]:
                    self._cache_text.append(self._text)

            if self.hover(window, camera):
                if MouseButton(1):
                    self._textMousePosition(window)
                    self.selected[0] = self._position
                    self._tt = True
            else:
                if MouseButton(1, True) and not self._tt:
                    self._State = False

            if MouseButton(1, True) and self._tt:
                self._textMousePosition(window)
                self.selected[1] = self._position
            else:
                self._tt = False

            # scroll
            _size = sdlttf.TTF_SizeUTF8(self._text_font, self.text[:self.column].encode())
            _loc_start = [_size[0] + 1 + self.scroll[0], _size[1] + 1]

            if _loc_start[0] > self._size[0]:
                self.scroll[0] -= _loc_start[0] - self._size[0]
            elif _loc_start[0] < 0:
                self.scroll[0] += -_loc_start[0] + 1

            if self._surface is not None:
                if self._surface.w > self._size[0]:
                    if 500 > (self.scroll[0] + 1 + self._surface.w):
                        self.scroll[0] += self._size[0] - (self.scroll[0] + self._surface.w)
                else:
                    self.scroll[0] = 0

    def drawObject(self, window, camera: Camera = None):
        if window.__WindowActive__:
            if self not in window.drawnObjects:
                window.drawnObjects.append(self)
                _render, cache_location, cache_size = _calculate_object2d(self._location, self._size, 0, (1, 1), window, camera, self._pivot)
                if _render:
                    sdl2.SDL_SetRenderDrawColor(self._surface_object_rd, 0, 0, 0, 0)
                    sdl2.SDL_RenderClear(self._surface_object_rd)

                    _texts = self.text

                    if self.selected[0] != self.selected[1]:
                        _size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[:self.selectedBox[0]].encode())
                        _ss = sdlttf.TTF_SizeUTF8(self._text_font, self.selectedText.encode())
                        sdlgfx.boxRGBA(self._surface_object_rd, _size[0] + self.scroll[0], 0, _size[0] + _ss[0] - 1 + self.scroll[0], _ss[1] - 1, 75, 75, 255, 170)

                    self._render()

                    if self._surface is not None:
                        self._text_surface_tx = sdl2.SDL_CreateTextureFromSurface(self._surface_object_rd, self._surface)
                        sdl2.SDL_SetTextureScaleMode(self._text_surface_tx, 1)
                        sdl2.SDL_RenderCopy(self._surface_object_rd, self._text_surface_tx, None, sdl2.SDL_Rect(self.scroll[0] + 1, self.scroll[1], self._surface.w, self._surface.h))
                        sdl2.SDL_DestroyTexture(self._text_surface_tx)

                    if self._State:
                        if self._p_timer.tickFlipFlop() or not self._p_start_timer.tick():
                            _size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[:self.column].encode())

                            _loc_start = [_size[0] + 1 + self.scroll[0], 1]
                            _loc_end = [_loc_start[0], _loc_start[1] + _size[1] - 3]

                            sdlgfx.thickLineRGBA(self._surface_object_rd, *_loc_start, *_loc_end, 2, 255, 255, 255, 255)

                    sdl2.SDL_RenderPresent(self._surface_object_rd)
                    window.blit(self._surface_object, cache_location, None, self._rotation)

    def hover(self, window: Window | InternalWindow, camera: Camera = None) -> bool:
        return object2dSimpleHover(window, camera, self._location, (self._size[0], self.surfaceSize[1]), (1, 1), self._pivot)

class ObjectInputTextBox(_ObjectInputText):
    def __init__(self, location=(0, 0), size=(200, 200), rotation: int = 0, font_size: int = 20, background_text: str = "", text: str = "", font=_DefaultFont):
        super().__init__(font_size, text, font)
        self._location = list(location)
        self._size = list(size)
        self._rotation = rotation
        self._rotation %= 360

        self._pivot = Pivot2D.TopLeftSide

        self._background_color = Color((0, 0, 0, 0))

        self._cursor = 1

        self._surface_object = sdl2.SDL_CreateRGBSurface(0, self._size[0]+2, self._size[1], 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000).contents
        self._surface_object_tx = None
        self._surface_object_rd = sdl2.SDL_CreateSoftwareRenderer(self._surface_object)

        self._text_surface_tx = None

        self._background_text = background_text
        self._time_text = Time(0.25)
        self._mouse_time_text = Time(0.1)

        self._copy_and_paste = True

        self._State = False

        self.scroll = [0, 0]

        self._text_render_type = 0

        self._tt = True

    @property
    def line(self):
        return self._text[:self._position].count("\n")

    @property
    def column(self):
        return self._position - sum(len(self._text.split("\n")[lo]) + 1 for lo in range(self.line))

    def update(self, window, camera: Camera = None):

        if self.hover(window, camera):
            _temp.MouseCursor = self._cursor
            if not self._State and MouseButton(1):
                self._State = self._tt = True
                self.selected[1] = self.selected[0] = self._textMousePosition(window)
        if self._State:
            if len(self._cache_text) >= 25:
                self._cache_text = self._cache_text[1:]

            if keyboard(KeyboardButton.Ctrl, True):
                if self._copy_and_paste:
                    if keyboard(KeyboardButton.KeyC):
                        _text = self.selectedText
                        SetClipboardText(_text if _text else self.text)
                    if keyboard(KeyboardButton.KeyV):
                        self._inputText(GetClipboardText())
                    if keyboard(KeyboardButton.KeyX):
                        _text = self.selectedText
                        SetClipboardText(_text if _text else self.text)
                        self.selected = self.selected if _text else [0, len(self.text)]
                        self._inputText("")

                if keyboard(KeyboardButton.KeyZ):
                    if len(self._cache_text) > 1:
                        self._text = str(self._cache_text[len(self._cache_text) - 2])
                        self._cache_text = self._cache_text[:-1]

            if keyboard(KeyboardButton.Shift):
                self.selected[0] = self._position
            if keyboard(KeyboardButton.Shift, True):
                self.selected[1] = self._position

            self._inputText(KeyboardText())

            click = KeyboardClick()
            if click is not None:
                self._p_start_timer.restart()
                self._p_timer.flipflop = True
                if click == KeyboardButton.Back:
                    if self.selected[0] != self.selected[1]:
                        self._inputText("")
                    else:
                        if self._position != len(self.text):
                            result = ''
                            for i, letra in enumerate(self.text):
                                if i == self._position if self._position <= len(self.text) - 1 else self._position <= len(self.text) - 1:
                                    result = result[:-1]
                                result += letra
                            self.text = result
                        else:
                            self.text = self.text[:-1]
                        self._position -= 1
                        self._render_cache = False

                elif click == KeyboardButton.Return:
                    self._inputText("\n")
                elif click == KeyboardButton.Tab:
                    self._inputText(" " * 4)

                # motion
                elif click in (KeyboardButton.Left, KeyboardButton.Right):
                    if click == KeyboardButton.Left:
                        self._position -= 1
                    elif click == KeyboardButton.Right:
                        self._position += 1
                    if not keyboard(KeyboardButton.Shift, True):
                        self.selected[0] = self.selected[1] = self._position

                elif click in (KeyboardButton.Up, KeyboardButton.Down):
                    _texts = self.text.split("\n")
                    _line = self.line

                    if (click == KeyboardButton.Up and _line != 0) or (click == KeyboardButton.Down and _line != len(_texts)-1):
                        _column = self._position - sum(len(_texts[lo]) + 1 for lo in range(_line))

                        if click == KeyboardButton.Up:
                            _n = sum(len(_texts[lo]) + 1 for lo in range(_line - 1 if _line > 0 else _line))
                            self._position = _n + min(_column, len(_texts[_line - 1]))
                        elif click == KeyboardButton.Down:
                            _n = sum(len(_texts[lo]) + 1 for lo in range(_line + 1))
                            self._position = _n + min(_column, len(_texts[_line + 1]))

                    if not keyboard(KeyboardButton.Shift, True):
                        self.selected[0] = self.selected[1] = self._position

            if self._position < 0:
                self._position = 0
            if self._position > len(self._text):
                self._position = len(self._text)

            if keyboard(-1, True):
                self._time_text.restart()
            if self._time_text.tick():
                if self._text != self._cache_text[len(self._cache_text) - 1]:
                    self._cache_text.append(self._text)

            if self.hover(window, camera):
                if MouseButton(1):
                    self._textMousePosition(window)
                    self.selected[0] = self._position
                    self._tt = True
            else:
                if MouseButton(1, True) and not self._tt:
                    self._State = False

            _texts = self.text.split("\n")
            _size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[self.line][:self.column].encode())
            _loc_start = [_size[0] + 1 + self.scroll[0], _size[1] * (self.line + 1) + self.scroll[1]]
            _line_size = _size[1] * len(_texts)

            if MouseButton(1, True) and self._tt:
                if self.hover(window, camera):
                    self._mouse_time_text.restart()
                    self._textMousePosition(window)
                    self.selected[1] = self._position
                else:
                    if self._mouse_time_text.tick(True):
                        self._textMousePosition(window)
                        self.selected[1] = self._position
            else:
                self._tt = False

            # scroll
            if click is not None or self._tt:
                # x
                if _loc_start[0] > self._size[0]:
                    self.scroll[0] -= _loc_start[0] - self._size[0]
                elif _loc_start[0] < 0:
                    self.scroll[0] += -_loc_start[0] + 1

                # y
                if _loc_start[1] > self._size[1]:
                    self.scroll[1] -= _loc_start[1] - self._size[1]
                elif _loc_start[1] < _size[1]:
                    self.scroll[1] += -_loc_start[1] + _size[1]

            # scroll x
            _s_size = sdlttf.TTF_SizeUTF8(self._text_font, self.text.encode())
            if self._surface is not None:
                if _s_size[0] > self._size[0]:
                    if self._size[0] > (self.scroll[0] + 1 + _s_size[0]):
                        self.scroll[0] += self._size[0] - (self.scroll[0] + _s_size[0])
                else:
                    self.scroll[0] = 0

            # scroll y
            if self.hover(window, camera):
                s = MouseScroll()
                if s != 0:
                    self.scroll[1] += s * 25
            if self.scroll[1] > 0 or self._size[1] - _line_size > 0:
                self.scroll[1] = 0
            elif self.scroll[1] < self._size[1] - _line_size:
                self.scroll[1] = self._size[1] - _line_size

    def drawObject(self, window, camera: Camera = None):
        if window.__WindowActive__:
            if self not in window.drawnObjects:
                window.drawnObjects.append(self)
                _render, cache_location, cache_size = _calculate_object2d(self._location, self._size, 0, (1, 1), window, camera, self._pivot)
                if _render:
                    sdl2.SDL_SetRenderDrawColor(self._surface_object_rd, 0, 0, 0, 0)
                    sdl2.SDL_RenderClear(self._surface_object_rd)

                    _texts = self.text.split("\n")

                    if self.selected[0] != self.selected[1]:
                        _selected_texts = self.selectedText.split("\n")

                        _line = self._text[:min(self.selected[0], self.selected[1])].count("\n")
                        _size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[_line][:self.selectedBox[0] - sum(len(self.text.split("\n")[lo]) + (1 if _line != 0 else 0) for lo in range(_line))].encode())

                        for num in range(len(_selected_texts)):
                            _loc = [_size[0] if num == 0 else 0, _size[1] * (_line + num)]
                            _ss = sdlttf.TTF_SizeUTF8(self._text_font, _selected_texts[num].encode())
                            sdlgfx.boxRGBA(self._surface_object_rd, _loc[0] + self.scroll[0], _loc[1] + self.scroll[1], _loc[0] + _ss[0] - 1 + self.scroll[0], _loc[1] + _ss[1] - 1 + self.scroll[1], 75, 75, 255, 170)

                    self._render()

                    if self._surface is not None:
                        self._text_surface_tx = sdl2.SDL_CreateTextureFromSurface(self._surface_object_rd, self._surface)
                        sdl2.SDL_SetTextureScaleMode(self._text_surface_tx, 1)
                        sdl2.SDL_RenderCopy(self._surface_object_rd, self._text_surface_tx, None, sdl2.SDL_Rect(self.scroll[0] + 1, self.scroll[1], self._surface.w, self._surface.h))
                        sdl2.SDL_DestroyTexture(self._text_surface_tx)

                    if self._State:
                        if self._p_timer.tickFlipFlop() or not self._p_start_timer.tick():
                            _size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[self.line][:self.column].encode())

                            _loc_start = [_size[0] + 1 + self.scroll[0], _size[1] * self.text[:self._position].count("\n") + 1 + self.scroll[1]]
                            _loc_end = [_loc_start[0], _loc_start[1] + _size[1] - 3]

                            sdlgfx.thickLineRGBA(self._surface_object_rd, *_loc_start, *_loc_end, 2, 255, 255, 255, 255)

                    sdl2.SDL_RenderPresent(self._surface_object_rd)
                    window.blit(self._surface_object, cache_location, None, self._rotation)

    def hover(self, window: Window | InternalWindow, camera: Camera = None) -> bool:
        return object2dSimpleHover(window, camera, self._location, self._size, (1, 1), self._pivot)

class ObjectInputPassLine(_ObjectInputText):
    def __init__(self, location=(0, 0), size=(200, 200), rotation: int = 0, font_size: int = 20, background_text: str = "", text: str = "", font=_DefaultFont):
        super().__init__(font_size, text, font)
        self._location = list(location)
        self._size = list(size)
        self._rotation = rotation
        self._rotation %= 360

        self._pass = ""
        self._passVisibility = False

        self._pivot = Pivot2D.TopLeftSide

        self._background_color = Color((0, 0, 0, 0))

        self._cursor = 1

        self._surface_object = sdl2.SDL_CreateRGBSurface(0, self._size[0] + 2, sdlttf.TTF_SizeUTF8(self._text_font, b" ")[1], 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000).contents
        self._surface_object_tx = None
        self._surface_object_rd = sdl2.SDL_CreateSoftwareRenderer(self._surface_object)

        self._text_surface_tx = None

        self._background_text = background_text
        self._time_text = Time(0.25)

        self._copy_and_paste = True

        self._State = False

        self._text_render_type = 0

        self.scroll = [0, 0]

        self._tt = True

    @property
    def passwordVisibility(self):
        return self._passVisibility

    @passwordVisibility.setter
    def passwordVisibility(self, visibility):
        self._passVisibility = visibility

    def _inputPass(self, text):
        if text is not None:
            if self.selected[0] != self.selected[1]:
                result = ''
                for i, letra in enumerate(self._pass):
                    if not self.selectedBox[0] <= i < self.selectedBox[1]:
                        result += letra
                if self.selectedBox[1] != len(self._pass):
                    result2 = ''
                    for i, letra in enumerate(result):
                        if i == self.selectedBox[0] if self.selectedBox[0] <= len(self._pass) - 1 else self.selectedBox[0] <= len(self._pass) - 1:
                            result2 += text
                        result2 += letra
                else:
                    result2 = result + text
                self._pass = result2

            elif self._position != len(self._pass):
                result = ''
                for i, letra in enumerate(self._pass):
                    if i == self._position if self._position <= len(self._pass) - 1 else self._position <= len(self._pass) - 1:
                        result += text
                    result += letra
                self._pass = result

            else:
                self._pass += text

            self.selected[1] = self.selected[0] = self._position = self.selectedBox[0] + len(text) if self.selected[0] != self.selected[1] else self._position + len(text)

    @property
    def selectedPass(self):
        result = ""
        for i, letra in enumerate(self._pass):
            if self.selectedBox[0] <= i < self.selectedBox[1]:
                result += letra
        return result

    @property
    def column(self):
        return self._position

    def update(self, window, camera: Camera = None):

        if self.hover(window, camera):
            _temp.MouseCursor = self._cursor
            if not self._State and MouseButton(1):
                self._State = self._tt = True
                self.selected[1] = self.selected[0] = self._textMousePosition(window)
        if self._State:
            _texts = self.text

            if len(self._cache_text) >= 25:
                self._cache_text = self._cache_text[1:]

            if keyboard(KeyboardButton.Ctrl, True):
                if self._copy_and_paste:
                    if keyboard(KeyboardButton.KeyC):
                        _text = self.selectedText
                        SetClipboardText(_text if _text else self.text)
                    if keyboard(KeyboardButton.KeyV):
                        self._inputPass(GetClipboardText())
                    if keyboard(KeyboardButton.KeyX):
                        _text = self.selectedText
                        SetClipboardText(_text if _text else self.text)
                        self.selected = self.selected if _text else [0, len(self.text)]
                        self._inputPass("")

                if keyboard(KeyboardButton.KeyZ):
                    if len(self._cache_text) > 1:
                        self._text = str(self._cache_text[len(self._cache_text) - 2])
                        self._cache_text = self._cache_text[:-1]

            if keyboard(KeyboardButton.Shift):
                self.selected[0] = self._position
            if keyboard(KeyboardButton.Shift, True):
                self.selected[1] = self._position

            self._inputPass(KeyboardText())

            click = KeyboardClick()
            if click is not None:
                self._p_start_timer.restart()
                self._p_timer.flipflop = True
                if click == KeyboardButton.Back:
                    if self.selected[0] != self.selected[1]:
                        self._inputPass("")
                    else:
                        if self._position != len(self._pass):
                            result = ''
                            for i, letra in enumerate(self._pass):
                                if i == self._position if self._position <= len(self._pass) - 1 else self._position <= len(self._pass) - 1:
                                    result = result[:-1]
                                result += letra
                            self._pass = result
                        else:
                            self._pass = self._pass[:-1]
                        self._position -= 1

                # motion
                elif click in (KeyboardButton.Left, KeyboardButton.Right):
                    if click == KeyboardButton.Left:
                        self._position -= 1
                    elif click == KeyboardButton.Right:
                        self._position += 1
                    if not keyboard(KeyboardButton.Shift, True):
                        self.selected[0] = self.selected[1] = self._position

                elif click in (KeyboardButton.Up, KeyboardButton.Down):
                    if not keyboard(KeyboardButton.Shift, True):
                        self.selected[0] = self.selected[1] = self._position

            if self._position < 0:
                self._position = 0
            if self._position > len(self._pass):
                self._position = len(self._pass)

            if keyboard(-1, True):
                self._time_text.restart()
            if self._time_text.tick():
                if self._pass != self._cache_text[len(self._cache_text) - 1]:
                    self._cache_text.append(self._pass)

            if self.hover(window, camera):
                if MouseButton(1):
                    self._textMousePosition(window)
                    self.selected[0] = self._position
                    self._tt = True
            else:
                if MouseButton(1, True) and not self._tt:
                    self._State = False

            if MouseButton(1, True) and self._tt:
                self._textMousePosition(window)
                self.selected[1] = self._position
            else:
                self._tt = False

            # scroll
            _size = sdlttf.TTF_SizeUTF8(self._text_font, self.text[:self.column].encode())
            _loc_start = [_size[0] + 1 + self.scroll[0], _size[1] + 1]

            if _loc_start[0] > self._size[0]:
                self.scroll[0] -= _loc_start[0] - self._size[0]
            elif _loc_start[0] < 0:
                self.scroll[0] += -_loc_start[0] + 1

            if self._surface is not None:
                if self._surface.w > self._size[0]:
                    if 500 > (self.scroll[0] + 1 + self._surface.w):
                        self.scroll[0] += self._size[0] - (self.scroll[0] + self._surface.w)
                else:
                    self.scroll[0] = 0

        masked_pass = self._pass if self._passVisibility else "*" * len(self._pass)
        if self._text != masked_pass:
            self._render_cache = False
            self._text = masked_pass

    def drawObject(self, window, camera: Camera = None):
        if window.__WindowActive__:
            if self not in window.drawnObjects:
                window.drawnObjects.append(self)
                _render, cache_location, cache_size = _calculate_object2d(self._location, self._size, 0, (1, 1), window, camera, self._pivot)
                if _render:
                    sdl2.SDL_SetRenderDrawColor(self._surface_object_rd, 0, 0, 0, 0)
                    sdl2.SDL_RenderClear(self._surface_object_rd)

                    _texts = self.text

                    if self.selected[0] != self.selected[1]:
                        _size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[:self.selectedBox[0]].encode())
                        _ss = sdlttf.TTF_SizeUTF8(self._text_font, self.selectedText.encode())
                        sdlgfx.boxRGBA(self._surface_object_rd, _size[0] + self.scroll[0], 0, _size[0] + _ss[0] - 1 + self.scroll[0], _ss[1] - 1, 75, 75, 255, 170)

                    self._render()

                    if self._surface is not None:
                        self._text_surface_tx = sdl2.SDL_CreateTextureFromSurface(self._surface_object_rd, self._surface)
                        sdl2.SDL_SetTextureScaleMode(self._text_surface_tx, 1)
                        sdl2.SDL_RenderCopy(self._surface_object_rd, self._text_surface_tx, None, sdl2.SDL_Rect(self.scroll[0] + 1, self.scroll[1], self._surface.w, self._surface.h))
                        sdl2.SDL_DestroyTexture(self._text_surface_tx)

                    if self._State:
                        if self._p_timer.tickFlipFlop() or not self._p_start_timer.tick():
                            _size = sdlttf.TTF_SizeUTF8(self._text_font, _texts[:self.column].encode())

                            _loc_start = [_size[0] + 1 + self.scroll[0], 1]
                            _loc_end = [_loc_start[0], _loc_start[1] + _size[1] - 3]

                            sdlgfx.thickLineRGBA(self._surface_object_rd, *_loc_start, *_loc_end, 2, 255, 255, 255, 255)

                    sdl2.SDL_RenderPresent(self._surface_object_rd)
                    window.blit(self._surface_object, cache_location, None, self._rotation)

    def hover(self, window: Window | InternalWindow, camera: Camera = None) -> bool:
        return object2dSimpleHover(window, camera, self._location, (self._size[0], self.surfaceSize[1]), (1, 1), self._pivot)
