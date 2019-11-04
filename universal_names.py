#!/usr/bin/env python
from misc_function import *
import pygame
pygame.mixer.pre_init(22100, -16, 2, 64)

#--various variable that are used throughout game--

hitbox = 'hitbox'

feet = 'feet'

head = 'head'

screen_width = 600

screen_height = 600

megaman_images = load_images('megaman_sprites')

megaman_sounds = load_sounds('audio/fx')

sfx_volume = 0.6

m7 = load_images('m7')