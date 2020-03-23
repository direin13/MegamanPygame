#!/usr/bin/env python
from misc_function import *
import pygame
from camera import *
from music_player import Song_player

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

checkpoint = [0, 0]
world_location = [0, 0]

songs = Song_player('1', ['audio/Concrete man.mp3', 'audio/Game Over.mp3', 'audio/Game Over Screen.mp3', 
                          'audio/Level intro sequence.mp3', 'audio/Title.mp3'], volume=0.7)

megaman_images = load_images('megaman_sprites')

projectiles = load_images('projectiles')

background_images = load_images('background')

misc_images = load_images('misc')

prop_images = load_images('props')

megaman_sounds = load_sounds('audio/fx')

sfx_volume = 0.6

camera_x, camera_y = 250, 200
camera = Camera(camera_x, camera_y)