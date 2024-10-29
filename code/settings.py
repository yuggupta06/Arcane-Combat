import pygame
import os
from os.path import join
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
pygame.init()
os.environ["SDL_VIDEO_CENTERED"]="1"
info =pygame.display.Info()
WINDOW_WIDTH, WINDOW_HEIGHT=info.current_w,info.current_h
TILE_SIZE=40
PlAYER_TILE_SIZE=64

def get_absolute_path(*path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__),"..",*path))
