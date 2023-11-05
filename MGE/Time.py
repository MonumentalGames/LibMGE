from time import time, sleep

__all__ = ["Time", "fps_to_time", "get_fps_from_time"]

class Time:
    def __init__(self, delta_time: int | float):
        self._tick_time = time()
        self._delta_time = delta_time
        self._elapsed_time = time() - self._tick_time
        self._flipflop_bool = False

    @property
    def delta_time(self) -> int | float:
        return self._delta_time

    @delta_time.setter
    def delta_time(self, delta_time: int | float):
        self._delta_time = delta_time

    def restart(self):
        self._tick_time = time()

    def tick(self, restart=False) -> bool:
        self._elapsed_time = time() - self._tick_time
        if self._elapsed_time >= self._delta_time:
            if restart:
                self.restart()
            return True
        return False

    def tickSleep(self):
        self._elapsed_time = time() - self._tick_time
        if self._elapsed_time < self._delta_time:
            sleep(self._delta_time - self._elapsed_time)
        self._tick_time = time()

    def tickMotion(self) -> float:
        self._elapsed_time = time() - self._tick_time
        self._tick_time = time()
        return 0.01 * ((self._elapsed_time / self._delta_time) * 100)

    def tickFlipFlop(self) -> bool:
        self._elapsed_time = time() - self._tick_time
        if self._elapsed_time >= self._delta_time:
            self.restart()
            self._flipflop_bool = not self._flipflop_bool
        return self._flipflop_bool

def fps_to_time(target_fps):
    return 0 if target_fps == 0 else 1.0 / target_fps

def get_fps_from_time(object_time: Time) -> int:
    return round(1 / object_time._elapsed_time if not object_time._elapsed_time == 0 else 1 / object_time._delta_time)
