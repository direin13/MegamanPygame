#!/usr/bin/env python
import pygame
import os
pygame.mixer.pre_init(44100, -16, 2, 512, allowedchanges=0)

def display_text(font, s, surf, colour, co_ordinates):
   text = font.render(s, False, colour) 
   return surf.blit(text, co_ordinates)

def load_images(directory):
   directory_images = {}

   for image in os.listdir(directory):
      try:
         directory_images[image.split('.')[0]] = pygame.image.load('{}/{}'.format(directory, image))
      except:
         pass

   return directory_images
      #--the name of the file(without the file extension) return to the loaded image itself e.g all_images[name] will return the loaded image of name.png--

def load_sounds(directory):
   directory_sounds = {}

   for sound in os.listdir(directory):
      try:
         directory_sounds[sound.split('.')[0]] = pygame.mixer.Sound('{}/{}'.format(directory, sound))
      except:
         pass

   return directory_sounds
   #--the name of the file(without the file extension) return to the loaded image itself e.g all_images[name] will return the loaded image of name.wav--

def play_sound(file_name, dictionary, channel=0, volume=1.0, loops=0):
   dictionary[file_name].set_volume(volume)
   pygame.mixer.Channel(channel).play(dictionary[file_name], loops=loops)

