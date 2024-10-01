import os
from math import cos, sin, radians
from .Log import LogError

def line_intersection(start_1, end_1, start_2, end_2):
    dx1 = end_1[0] - start_1[0]
    dy1 = end_1[1] - start_1[1]
    dx2 = end_2[0] - start_2[0]
    dy2 = end_2[1] - start_2[1]

    det = dx1 * dy2 - dy1 * dx2

    if det == 0:
        return None

    u = ((start_2[0] - start_1[0]) * dy2 - (start_2[1] - start_1[1]) * dx2) / det
    v = ((start_2[0] - start_1[0]) * dy1 - (start_2[1] - start_1[1]) * dx1) / det

    if 0 <= u <= 1 and 0 <= v <= 1:
        intersection_x = start_1[0] + u * dx1
        intersection_y = start_1[1] + u * dy1
        return (round(intersection_x), round(intersection_y))
    else:
        return None

def rotate_point(x, y, cx, cy, angle):
    angle_rad = radians(angle)

    dx = x - cx
    dy = y - cy

    new_x = dx * cos(angle_rad) - dy * sin(angle_rad) + cx
    new_y = dx * sin(angle_rad) + dy * cos(angle_rad) + cy

    return new_x, new_y

def calculate_square_vertices(location, size, rotation_angle):
    x, y = location
    width, height = size

    cx = x + width / 2
    cy = y + height / 2

    vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]

    if rotation_angle != 0:
        vertices = [rotate_point(v[0], v[1], cx, cy, rotation_angle) for v in vertices]

    return vertices

def edges(vertices):
    _edges = [(vertices[num], vertices[num+1 if num+1 <= len(vertices)-1 else 0]) for num in range(len(vertices))]
    return _edges

class Mesh2D:
    def __init__(self, vertices: list):
        self._vertices = vertices
        self._edges = []
        self._faces = []

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return [(self._vertices[num], self._vertices[num+1 if num+1 <= len(self._vertices)-1 else 0]) for num in range(len(self._vertices))]

def LoadObj(path):
    vertices = []
    if os.path.exists(path):
        with open(path) as obj:
            r = obj.read()
            for rr in r.split("\n"):
                if len(rr) > 0 and rr[0] == "v":
                    r2 = rr.split()
                    vertices.append((int(float(r2[1]) * 100), int(float(r2[3] if len(r2) == 4 else r2[2]) * 100)))
    if len(vertices) == 0:
        LogError(f"{path}")
    return Mesh2D(vertices)

def CreateMeshPlane(size):
    return Mesh2D([(0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])])
