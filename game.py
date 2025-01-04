from mesh import *
from projection import ProjectionViewer
import pygame
from pygame.locals import *

pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 120
MODE = "perspective"

cube0 = UnitCube(-100, 100)
viewer = ProjectionViewer(WIDTH, HEIGHT, FPS, MODE)
viewer.addMesh("Unit Cube", cube0)

viewer.run()