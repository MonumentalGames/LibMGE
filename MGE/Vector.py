from numpy import deg2rad, cos, sin

__all__ = ["simpleMotion", "object2dSimpleMotion"]

def simpleMotion(location, theta, axis, speed=0):
    theta_rad = deg2rad((theta + 90 * axis) * -1)

    dx = speed * cos(theta_rad)
    dy = speed * sin(theta_rad)

    return [(location[0] + -dx), (location[1] + dy)]

def object2dSimpleMotion(object, axis, speed=0):
    if "speed" in object.variables:
        if object.variables["speed"] != 0:
            speed = object.variables["speed"]

    return simpleMotion(object.location, object.rotation, axis, speed)
