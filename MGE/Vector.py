import numpy as np

class Vector:
    X = 1
    Y = 2

    GLOBAL = 10
    LOCAL = 30

def motion(object2d, axis, speed=0):
    x, y = object2d.localization
    theta = object2d.rotation

    # Conversão do ângulo de graus para radianos
    theta_rad = np.deg2rad((theta + 90 * axis) * -1)

    try:
        if object2d.variables["speed"] != 0:
            speed = object2d.variables["speed"]
    except:
        pass

    # Cálculo das componentes horizontal e vertical do vetor de movimento
    dx = speed * np.cos(theta_rad)
    dy = speed * np.sin(theta_rad)

    return [(x + dx), (y + dy)]
