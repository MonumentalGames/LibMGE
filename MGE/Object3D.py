import pygame
import threading
from .MGE import Program
from .Vector import motion
from .Material import Material
from .Mesh import *

class Pivot3D:
    CENTER = 801
    #TOP_LEFT_SIDE = 700
    #TOP_RIGHT_SIDE = 750
    #LOWER_LEFT_SIDE = 600
    #LOWER_RIGHT_SIDE = 650

class Object3D:
    def __init__(self, localization=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), mesh=Mesh(cube)):
        self.localization = localization
        self.rotation = rotation
        self.scale = scale
        self.Mesh = mesh
        self.material = Material()
        self.variables = {}

        self.object_render = False
        self.always_render = False

        self.cache_object = None

    def draw_object(self, screen, camera=None, pivot=Pivot3D.CENTER):
        pass

    def set_localization(self, localization):
        self.localization = localization

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.object_render = False
        if self.material is not None:
            self.material.object_render = False

    def set_scale(self, scale):
        self.scale = scale
        self.object_render = False
        if self.material is not None:
            self.material.object_render = False

    def set_material(self, material: Material):
        self.material = material
        self.object_render = False
        self.material.object_render = False

    def get_localization(self):
        pass

    def get_size(self):
        pass

    def motion(self, axis, axis_type, speed):
        Program.Temp.ForceRender = True
        if axis_type == 10:  # global
            if axis == 1:  # x
                self.localization[0] += speed
            if axis == 2:  # y
                self.localization[1] += speed
            if axis == 3:  # z
                self.localization[2] += speed
        if axis_type == 30:  # local
            self.localization = motion(self, axis, speed)

