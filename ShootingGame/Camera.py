import pygame
import System

class Camera(System.System):
    def __init__(self):
        self.CameraPos = pygame.math.Vector2(0, 0)
        
    def CameraMove(self, dx, dy):
        pass