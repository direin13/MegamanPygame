#!/usr/bin/env python
import pygame
from timer import Timer

class Bit_text(object):
   """used to display text in 8 bit font"""

   #each letter is made up of scaled rectangles along the x and y axis.
   #char_list[i] = y pos, char_list[i][j] = x pos
   #all the chars don't surpass 6 pixels in width/height for this game, but you can
   #add your own.

   char_list = {'.': [[], [], [], [], [], [0, 1], [0, 1]],
               '(': [[3, 4], [1, 2], [0, 1], [0], [0, 1], [1, 2], [3, 4]],
               ')': [[3, 2], [5, 4], [6, 5], [6], [6, 5], [5, 4], [3, 2]],
               '©': [[2, 3, 4], [1, 5], [0, 3, 4, 6], [0, 2, 6], [0, 3, 4, 6], [1, 5], [2, 3, 4]],
               ',': [[], [], [], [2, 3], [2, 3], [3], [2]],
               '-': [[], [], [], [0, 1, 2, 3, 4, 5, 6], [], [], []],
               '_': [[], [], [], [], [], [], [0, 1, 2, 3, 4, 5, 6]],
               ':': [[3, 4], [3, 4], [], [], [], [3, 4], [3, 4]],
               '>': [[0,1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 1, 2], [0, 1]],
               '0': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 4, 5, 6], [0, 1, 3, 5, 6], [0, 1, 2, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               '1': [[2, 3, 4], [1, 2, 3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4]],
               '2': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [5, 6], [3, 4, 5], [1, 2], [0, 1], [0, 1, 2, 3, 4, 5, 6]],
               '3': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [5, 6], [2, 3, 4, 5], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               '4': [[0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 2, 3, 4, 5, 6], [4, 5], [4, 5]],
               '5': [[0, 1, 2, 3, 4, 5, 6], [0, 1], [0, 1, 2, 3, 4, 5], [5, 6], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               '6': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1], [0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               '7': [[0, 1, 2, 3, 4, 5, 6], [5, 6], [4, 5], [3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4]],
               '8': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               '9': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5, 6], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               'a': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
               'b': [[0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5]],
               'c': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1], [0, 1], [0, 1], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               'd': [[0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5]],
               'e': [[0, 1, 2, 3, 4, 5, 6], [0, 1], [0, 1], [0, 1, 2, 3, 4, 5], [0, 1], [0, 1], [0, 1, 2, 3, 4, 5, 6]],
               'f': [[0, 1, 2, 3, 4, 5, 6], [0, 1], [0, 1], [0, 1, 2, 3, 4, 5], [0, 1], [0, 1], [0, 1]],
               'g': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1], [0, 1, 3, 4, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               'h': [[0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
               'i': [[3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4]],
               'j': [[4, 5], [4, 5], [4, 5], [4, 5], [1, 2, 4, 5], [1, 2, 4, 5], [2, 3, 4]],
               'k': [[0, 1, 4, 5], [0, 1, 3, 4], [0, 1, 2, 3], [0, 1, 2], [0, 1, 2, 3], [0, 1, 3, 4], [0, 1, 4, 5]],
               'l': [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1, 2, 3, 4, 5]],
               'm': [[0, 1, 5, 6], [0, 1, 2, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6], [0, 1, 3, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
               'n': [[0, 1, 5, 6], [0, 1, 2, 5, 6], [0, 1, 2, 3, 5, 6], [0, 1, 3, 4, 5, 6], [0, 1, 4, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
               'o': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               'p': [[0, 1, 2, 3, 4, 5], [0, 1, 5, 6,], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5], [0, 1], [0, 1]],
               'q': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 3, 4, 5, 6], [0, 1, 4, 5, 6], [1, 2, 3, 4, 5]],
               'r': [[0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5], [0, 1, 4, 5], [0, 1, 5, 6]],
               's': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1], [1, 2, 3, 4, 5], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               't': [[0, 1, 2, 3, 4, 5], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3]],
               'u': [[0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
               'v': [[0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 4, 5], [2, 3, 4], [3]],
               'w': [[0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 3, 5, 6], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 4, 5, 6], [0, 1, 5, 6]],
               'x': [[1, 2, 5, 6], [1, 2, 5, 6], [2, 3, 4, 5], [3, 4], [2, 3, 4, 5], [1, 2, 5, 6], [1, 2, 5, 6]],
               'y': [[0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5], [1, 2, 3, 4], [2, 3], [2, 3], [2, 3]],
               'z': [[0, 1, 2, 3, 4, 5], [0, 4, 5], [3, 4], [2, 3], [1, 2], [0, 1, 5], [0, 1, 2, 3, 4, 5]],
               ' ': [[], [], [], [], [], [], []]}

   def __init__(self, string, x, y, width, height, colour=(255,255,255), pattern_interval=30):
      self.string = string
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.colour = colour
      self.pattern_timers = Timer()
      self.pattern_timers.add_ID('flash_interval', pattern_interval)
      self.pattern_timers.add_ID('add_letter_interval', pattern_interval)
      self.pattern_interval = pattern_interval
      self.show_letters_up_to = 0
   

   def flash(self, surf, pattern_interval=None):
      if pattern_interval != None:
         self.pattern_timers.all_timers['flash_interval']['origin'] = pattern_interval

      if self.pattern_timers.is_almost_finished('flash_interval', self.pattern_timers.get_ID('flash_interval')['origin']//2) != True:
         Bit_text.display_text(surf, (self.x,self.y), self.string, self.width, self.height, self.colour)

      elif self.pattern_timers.is_finished('flash_interval'):
         self.pattern_timers.replenish_timer('flash_interval', self.pattern_interval)

      self.pattern_timers.countdown('flash_interval')


   def show_letter_sequence(self, surf, pattern_interval=None):
      if pattern_interval != None:
         self.pattern_timers.all_timers['add_letter_interval']['origin'] = pattern_interval
      s = self.string[0:self.show_letters_up_to]
      if self.show_letters_up_to == len(self.string):
         s = self.string
      else:
         if self.pattern_timers.is_finished('add_letter_interval') != True:
            self.pattern_timers.countdown('add_letter_interval')
         else:
            self.show_letters_up_to += 1
            self.pattern_timers.replenish_timer('add_letter_interval', self.pattern_interval)
            
      Bit_text.display_text(surf, (self.x,self.y), s, self.width, self.height, self.colour)


   def display(self, surf, pattern=None, pattern_interval=None, min_char_width=6, char_seperation=2):
      if pattern == None:
         Bit_text.display_text(surf, (self.x,self.y), self.string, self.width, self.height, self.colour,
                               min_char_width, char_seperation)
      elif pattern == 'flash':
         self.flash(surf, pattern_interval)
      elif pattern == 'letter_sequence':
         self.show_letter_sequence(surf, pattern_interval)


   @staticmethod
   def display_text(surf, coordinates, string, width=1, height=1, colour=(255,255,255), min_char_width=6, char_seperation=2):
      """Display String on a surface.
         Width and Height refer to width and height of each pixel (rectangle) per letter
         """

      all_chars = list(str(string))
      x_pos_offset = 0 #where each character will be drawn

      for char in all_chars:
         y = coordinates[1]
         longest_pixel_x = 0
         for pixel_array in Bit_text.char_list[char.lower()]: #going through every pixel_array in 
                                                              #characters and making a rectangle at 
                                                              #each number in the pixel_array
            if len(pixel_array) != 0:
               for i in range(len(pixel_array)):
                  x = coordinates[0] + (pixel_array[i] * width) + x_pos_offset
                  pygame.draw.rect(surf, colour, (x, y, width, height))
                  if pixel_array[i] > longest_pixel_x:
                     longest_pixel_x = pixel_array[i]

            y += height
         if longest_pixel_x < min_char_width:
            longest_pixel_x = min_char_width
         x_pos_offset += (longest_pixel_x + char_seperation) * width


