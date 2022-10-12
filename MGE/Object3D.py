import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Object3D:
    def __init__(self, model):
        self.model = model
        self.material = None
