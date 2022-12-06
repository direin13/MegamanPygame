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

songs = Song_player('1', ['resources/audio/Concrete Man.mp3', 'resources/audio/Game Over.mp3', 'resources/audio/Game Over Screen.mp3', 
                          'resources/audio/Level intro sequence.mp3', 'resources/audio/Title.mp3', 'resources/audio/Boss theme.mp3', 
                          'resources/audio/Victory theme.mp3'], volume=0.7)

megaman_images = load_images('resources/megaman_sprites')

projectiles = load_images('resources/projectiles')

background_images = load_images('resources/background')

misc_images = load_images('resources/misc')

prop_images = load_images('resources/props')

megaman_sounds = load_sounds('resources/audio/fx')

sfx_volume = 0.6
