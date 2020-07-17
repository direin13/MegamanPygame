#!/usr/bin/env python
import pygame
import sprite
from megaman_object import Megaman_object
import universal_var
from timer import Timer
from misc_function import play_sound

class Energy_bar(Megaman_object):
   def __init__(self, ID, x, y, points, colour1=(200,200,200), colour2=(255,255,255)):
      self.scale_factor = [6, 3] #[0] = width, [1] = height
      width = 4
      height = 56
      bar_outline = sprite.Sprite(universal_var.main_sprite, x, y, width * self.scale_factor[0], height * self.scale_factor[1], 
                                 [(universal_var.main_sprite, [universal_var.misc_images['bar']], 1)])

      super().__init__(ID, x, y, [bar_outline], None, False, width, height)
      self.display_layer = 5
      self.points = points
      self.original_points = points

      self.energy_rect_width = width  #rect refers to energy bar that's coloured
      self.energy_rect_height = height
      self.colour1 = colour1
      self.colour2 = colour2
      self.all_timers.add_ID('time_till_increment', 2)
      self.all_timers.add_ID('play_sound', 3)


   def display(self, surf):
      if self.is_active:
         if self.points <= 0: #If points has dropped to zero then I don't want it to go into minus
            self.points = 0
            self.energy_rect_height = 0
            height_accum = self.original_points

         elif self.points >= self.original_points:
            self.points = self.original_points
            self.energy_rect_height = self.height
            height_accum = 0

         else: #This formula gives the height the rectangle(health bar energy) has to be to match the original points - current points percentage
            points_diff = self.original_points - self.points
            bar_decrate = round(self.original_points/self.height)
            height_accum = round(points_diff / bar_decrate)
            self.energy_rect_height = self.height - height_accum

         rect_y = self.y + (height_accum * self.scale_factor[1])
         width = self.energy_rect_width * self.scale_factor[0]
         height = self.energy_rect_height * self.scale_factor[1]

         pygame.draw.rect(surf, (0, 0, 0), (self.x, self.y, self.width * self.scale_factor[0], self.height * self.scale_factor[1])) # black box in at the back
         if height_accum < self.original_points:
            pygame.draw.rect(surf, self.colour1, (self.x, rect_y, width, height)) #this is the rectangle within the bar that represents the points
            pygame.draw.rect(surf, self.colour2, (self.x + (width//3) + 1, rect_y, width // 4, height)) #this is second rectangle with rectangle 1

         Megaman_object.display(self, surf) #Blackbox outline that surrounds the rectangle health


   def refill(self, amount=1):
      if self.all_timers.is_finished('play_sound') != True:
         self.all_timers.countdown('play_sound')
      else:
         play_sound('health_regeneration', universal_var.megaman_sounds, channel=4, volume=universal_var.sfx_volume - 0.2)
         self.all_timers.replenish_timer('play_sound')

      if self.all_timers.is_finished('time_till_increment'):
         self.all_timers.replenish_timer('time_till_increment')
      else:
         self.all_timers.countdown('time_till_increment')

      if self.is_full() != True and self.all_timers.is_full('time_till_increment'):
         self.points += amount
         return True
      else:
         return False


   def is_full(self):
      return self.points == self.original_points

   def is_empty(self):
      return self.points <= 0


   def update(self):
      if universal_var.game_reset:
         self.is_active = False
      pass