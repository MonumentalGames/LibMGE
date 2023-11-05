import numpy

__all__ = ["motion"]

def motion(object, axis, speed=0):
    x, y = object.location
    theta = object.rotation

    # Conversão do ângulo de graus para radianos
    theta_rad = numpy.deg2rad((theta + 90 * axis) * -1)

    if "speed" in object.variables:
        if object.variables["speed"] != 0:
            speed = object.variables["speed"]

    # Cálculo das componentes horizontal e vertical do vetor de movimento
    dx = speed * numpy.cos(theta_rad)
    dy = speed * numpy.sin(theta_rad)

    return [(x + -dx), (y + dy)]
