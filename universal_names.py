#!/usr/bin/env python
from misc_function import *
import pygame
from camera import *
pygame.mixer.pre_init(22100, -16, 2, 64)

#--various variable that are used throughout game--

hitbox = 'hitbox'

feet = 'feet'

head = 'head'

main_sprite = 'main_sprite'

game_reset = False

game_pause = False

debug = False

screen_width = 600

screen_height = 600

checkpoint = [0, 0] #change this to change checkpoint
world_location = [0, 0] #This will basically tell the game how to get back to the checkpoint

megaman_images = load_images('megaman_sprites')

background_images = load_images('background')

effect_images = load_images('effects')

prop_images = load_images('props')

enemies = load_images('enemies')

megaman_sounds = load_sounds('audio/fx')

sfx_volume = 0.6

m7 = load_images('m7')

camera_x, camera_y = 250, 200
camera = Camera(camera_x, camera_y)