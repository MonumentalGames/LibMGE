import math
import os
from .Log import LogError

def line_intersection(start_1, end_1, start_2, end_2):
    # Calcula os deltas para as duas linhas
    dx1 = end_1[0] - start_1[0]
    dy1 = end_1[1] - start_1[1]
    dx2 = end_2[0] - start_2[0]
    dy2 = end_2[1] - start_2[1]

    # Calcula os determinantes
    det = dx1 * dy2 - dy1 * dx2

    # Verifica se as linhas são paralelas
    if det == 0:
        return None  # As linhas são paralelas ou coincidentes

    # Calcula os parâmetros 'u' e 'v' para encontrar o ponto de interseção
    u = ((start_2[0] - start_1[0]) * dy2 - (start_2[1] - start_1[1]) * dx2) / det
    v = ((start_2[0] - start_1[0]) * dy1 - (start_2[1] - start_1[1]) * dx1) / det

    # Verifica se o ponto de interseção está dentro das linhas
    if 0 <= u <= 1 and 0 <= v <= 1:
        intersection_x = start_1[0] + u * dx1
        intersection_y = start_1[1] + u * dy1
        return (round(intersection_x), round(intersection_y))
    else:
        return None  # As linhas não se intersectam dentro dos segmentos

def rotate_point(x, y, cx, cy, angle):
    # Converte o ângulo para radianos
    angle_rad = math.radians(angle)

    # Calcula a diferença entre as coordenadas e o ponto central
    dx = x - cx
    dy = y - cy

    # Aplica a rotação
    new_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad) + cx
    new_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad) + cy

    return new_x, new_y

def calculate_square_vertices(location, size, rotation_angle):
    x, y = location
    width, height = size

    # Calcula o ponto central
    cx = x + width / 2
    cy = y + height / 2

    # Define os vértices
    vertices = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]

    # Aplica a rotação a cada vértice
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
