#!/usr/bin/env python
import pygame
import sprite
import megaman_object
import universal_names

class Bar(megaman_object.Megaman_object):
   def __init__(self, ID, x, y, points, colour=(255,0,0)):
      self.scale_factor = (6, 3) #[0] = width, [1] = height
      width = 4
      height = 56
      bar_sprite = sprite.Sprite(universal_names.main_sprite, x, y, width * self.scale_factor[0], height * self.scale_factor[1], 
                                 [(universal_names.main_sprite, [universal_names.effect_images['bar']], 1)])

      super().__init__(ID, x, y, [bar_sprite], None, True, width, height)
      self.display_layer = 4
      self.points = points
      self.original_points = points

      self.rect_width = width  #rect refers to energy bar that's coloured
      self.rect_height = height
      self.colour1 = colour
      a = []
      for n in colour:
         if n + 80 > 255:
            n = 255
         else:
            n += 80
         a.append(n)
      self.colour2 = (a[0], a[1], a[2])

      self.bar_incrate = round(points/height) #This is the rate at which I add or minus a bar of energy. e.g If rate was 5, then every +-5 points I add or minus a bar


   def display(self, surf):
      if self.points <= 0: #If points has dropped to zero then I don't want it to go into minus
         self.points = 0
         self.rect_height = 0
         height_accum = self.original_points

      elif self.points >= self.original_points:
         self.points = self.original_points
         self.rect_height = self.height
         height_accum = 0

      else: #This formula will give me the height my rectangle(health bar energy) has to be to match the original points - current points percentage
         points_diff = self.original_points - self.points
         height_accum = round(points_diff / self.bar_incrate)
         self.rect_height = self.height - height_accum

      y = self.y + (height_accum * self.scale_factor[1])
      width = self.rect_width * self.scale_factor[0]
      height = self.rect_height * self.scale_factor[1]

      pygame.draw.rect(surf, (0, 0, 0), (self.x, self.y, self.width * self.scale_factor[0], self.height * self.scale_factor[1])) # black box in at the back
      if height_accum < self.original_points:
         pygame.draw.rect(surf, self.colour1, (self.x, y, width, height)) #this is the rectangle within the bar that represents the points
         pygame.draw.rect(surf, self.colour2, (self.x + (width//3) + 1, y, width // 4, height)) #this is second rectangle with rectangle 1

      megaman_object.Megaman_object.display(self, surf) #Blackbox outline that surrounds the rectangle health


   def update(self):
      pass