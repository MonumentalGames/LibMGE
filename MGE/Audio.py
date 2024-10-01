import os
from threading import Thread

from ._sdl import sdlmixer
from .Log import LogError

__all__ = ["Sound", "Music"]

class Sound:
    def __init__(self, path, preload=True):
        self._path = path
        self.sound = None
        self._channel = 0
        self._volume = 100
        self._load_type = 0
        if preload:
            self.load()

    def _threading_load(self, path):
        _threading = Thread(target=self._load, args=(path, ))
        _threading.daemon = True
        _threading.start()

    def _load(self, path):
        self._path = path if path is not None else self._path
        if os.path.exists(self._path):
            self.sound = sdlmixer.Mix_LoadWAV(self._path.encode())
        if not self.sound:
            LogError(f"Unable to load sound '{self._path}'")

    def load(self, path=None):
        if self._load_type == 0:
            self._threading_load(path)
        elif self._load_type == 1:
            self._load(path)

    def play(self, loops=-1):
        sdlmixer.Mix_PlayChannel(self._channel, self.sound, loops)

    def pause(self):
        sdlmixer.Mix_Pause(self._channel)

    def resume(self):
        sdlmixer.Mix_Resume(self._channel)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume
        sdlmixer.Mix_VolumeChunk(self.sound, self._volume)

class Music:
    def __init__(self, path):
        if os.path.exists(path):
            self.music = sdlmixer.Mix_LoadMUS(path.encode())
        else:
            LogError(f"Unable to load sound '{path}'")
        self._volume = 100

    def play(self, loops=-1):
        sdlmixer.Mix_PlayMusic(self.music, loops)

    def pause(self):
        sdlmixer.Mix_PauseMusic()

    def resume(self):
        sdlmixer.Mix_ResumeMusic()

    @property
    def position(self):
        return round(sdlmixer.Mix_GetMusicPosition(self.music))

    @position.setter
    def position(self, position):
        sdlmixer.Mix_SetMusicPosition(position)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume
        sdlmixer.Mix_VolumeMusic(self._volume)
