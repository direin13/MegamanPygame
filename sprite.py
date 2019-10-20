#!/usr/bin/env python
import threading
import pygame
import os

class Sprite(object):

   def __init__(self, x, y, width, height, active_frames=None, current_frame=0):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      #--make sure the active frames are in the order you want in a list--
      #--active_frames should contain a list of tuples. For each tuple, tuple[0] is the string name of the set of animations and tuple[1] are the images themselves--
      #--e.g active_frame = [('random_animation_1', [picture_1, picture_2, picture_3]), ('random_animation_2', [picture_4])]
      self.active_frames = active_frames
      if active_frames != None:
         self.all_frames = {}
         for frames in self.active_frames:
            self.all_frames[frames[0]] = frames[1]

         self.current_frame = current_frame
         self.current_animation = self.active_frames[0][0]
         self.flag = 0

   def display_animation(self, surf, frame_name):
      #--displays animations--
      if self.active_frames != None:
         if self.current_animation == frame_name:
            pass
         else:
            self.current_animation = frame_name
            self.current_frame = 0
         frame = pygame.transform.scale(self.all_frames[frame_name][self.current_frame], (self.width, self.height))
         surf.blit(frame, (self.x, self.y))
      else:
         print('you need "active_frames" to use display_animation()')

   def update(self, frame_speed):
      #--used to cycle through the sprite's animations
      if self.active_frames != None:
         frame_per_update = frame_speed // len(self.all_frames[self.current_animation])

         if self.flag >= frame_per_update:
            self.flag = 0
            self.current_frame += 1
         else:
            self.flag += 1

         if self.current_frame >= len(self.all_frames[self.current_animation]):
            self.current_frame = 0
      else:
         print('you need "active_frames" to use update()')

#--------------------------------------------------------------------

class Collision_box(object):

   def __init__(self, ID, x, y, collision_width, collision_height, colour=(255,0,0), x_offset=0, y_offset=0):
      #--In pygame, a surface's x and y co_ordinate starts from the top left corner which I felt was inconvenient for collision boxes, so here the x and y starts at the middle of the box

      self.ID = ID
      self.x_offset = x_offset
      self.y_offset = y_offset
      self.x = x + (collision_width // 2) + self.x_offset
      self.y = y + (collision_height // 2) + self.y_offset
      self.collision_width = collision_width
      self.collision_height = collision_height
      self.colour = colour
      self.left_edge = self.x - (collision_width // 2)
      self.right_edge = self.x + (collision_width // 2)
      self.top_edge = self.y - (collision_height // 2)
      self.bottom_edge = self.y + (collision_height // 2)
      self.box = pygame.Surface((self.collision_width, self.collision_height))



   def display_collbox(self, surf, alpha=100):
      self.box.set_alpha(alpha)
      self.box.fill(self.colour)
      surf.blit(self.box, (self.x - (self.collision_width//2), self.y - (self.collision_height//2)))
      pygame.draw.circle(surf, (0, 0, 0), (self.left_edge, self.y), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.right_edge, self.y), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.x, self.top_edge), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.x, self.bottom_edge), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.x, self.y), 2)


   def collision(self, x, y):
      if (x >= self.left_edge and x <= self.right_edge):
         if (y >= self.top_edge and y <= self.bottom_edge):
            return True
         else:
            pass
      return False



   def collision_sprite(self, other):
      #--this checks if another Collison_box object is colliding with the self and returns True or False--

      #--is self's collision box (left, right, top or bottom edge) is inside other's collision box (between his left or right and top or bottom edge)?
      if (self.right_edge <= other.right_edge and self.right_edge >= other.left_edge) or (self.left_edge >= other.left_edge and self.left_edge <= other.right_edge):
         if (self.top_edge >= other.top_edge and self.top_edge <= other.bottom_edge) or (self.bottom_edge <= other.bottom_edge and self.bottom_edge >= other.top_edge):
            return True
         elif other.x > self.left_edge and other.x < self.right_edge and other.y > self.top_edge and other.y < self.bottom_edge:
            return True
      elif other.x > self.left_edge and other.x < self.right_edge and other.y > self.top_edge and other.y < self.bottom_edge:
         return True

      #--if not then is other's collision box inside self's collision box?
      if (other.right_edge <= self.right_edge and other.right_edge >= self.left_edge) or (other.left_edge >= self.left_edge and other.left_edge <= self.right_edge):
         if (other.top_edge >= self.top_edge and other.top_edge <= self.bottom_edge) or (other.bottom_edge <= self.bottom_edge and other.bottom_edge >= self.top_edge):
            return True
         elif self.x > other.left_edge and self.x < other.right_edge and self.y > other.top_edge and self.y < other.bottom_edge:
            return True
      elif self.x > other.left_edge and self.x < other.right_edge and self.y > other.top_edge and self.y < other.bottom_edge:
            return True
      return False


#---------------------------------------------------

class Sprite_surface(object):
   all_sprite_surfaces = {}
   all_name_index = {}

   def __init__(self, ID, x, y, sprite=None, coll_boxes=None):
      if ID in Sprite_surface.all_name_index:
         Sprite_surface.all_name_index[ID] += 1
         self.ID = '{}-{}'.format(ID, Sprite_surface.all_name_index[ID])
      else:
         Sprite_surface.all_name_index[ID] = 0
         self.ID = '{}-{}'.format(ID, Sprite_surface.all_name_index[ID])

      self.x = x
      self.y = y
      self.all_collboxes = {}
      self.sprite = sprite
      if coll_boxes == None:
            pass
      else:
         for coll_box in coll_boxes:
            self.all_collboxes[coll_box.ID] = coll_box
      Sprite_surface.all_sprite_surfaces[self.ID] = self



   def display_collboxes(self, screen, alpha=100):
      for collbox in self.all_collboxes.values():
         collbox.display_collbox(screen, alpha)


   def update(self):
      try:
         for coll_box in self.all_collboxes.values():
            coll_box.x = self.x + (coll_box.collision_width // 2) + coll_box.x_offset
            coll_box.y = self.y + (coll_box.collision_height // 2) + coll_box.y_offset
            coll_box.left_edge = coll_box.x - (coll_box.collision_width // 2)
            coll_box.right_edge = coll_box.x + (coll_box.collision_width // 2)
            coll_box.top_edge = coll_box.y - (coll_box.collision_height // 2)
            coll_box.bottom_edge = coll_box.y + (coll_box.collision_height // 2)
      except ValueError:
         pass
      try:
         self.sprite.x = self.x
         self.sprite.y = self.y
      except AttributeError:
         pass

   def add_collbox(self, ID, x, y, collision_width, collision_height, x_offset=0, y_offset=0):
      box = Collision_box(ID, x, y, collision_width, collision_height, x_offset, y_offset)
      self.all_collboxes[box.ID] = box
      
#----------------------------------------------------------------

class Camera(object):
   def __init__(self, x, y, static=True):
      self.x = x
      self.y = y
      self.static = static

   def get_pos_x(self, sprite_surf):
      if sprite_surf.x < self.x:
         return 0
      elif sprite_surf.x > self.x:
         return 1
      else:
         return 2

   def get_pos_y(self, sprite_surf):
      if sprite_surf.y < self.y:
         return 0
      elif sprite_surf.y > self.y:
         return 1
      else:
         return 2

   def follow_x(self, main_sprite_surf, speed=None):
      dist = self.x - main_sprite_surf.x

      if self.get_pos_x(main_sprite_surf) != 2 and self.static == False:
         for sprite_surf in Sprite_surface.all_sprite_surfaces.values():
            if speed == None:
               sprite_surf.x += dist
            else:
               sprite_surf.x += speed
      else:
         pass

   def follow_y(self, main_sprite_surf, speed=None):
      dist = self.y - main_sprite_surf.y

      if self.get_pos_y(main_sprite_surf) != 2 and self.static == False:
         for sprite_surf in Sprite_surface.all_sprite_surfaces.values():
            if speed == None:
               sprite_surf.y += dist
            else:
               sprite_surf.y += speed
      else:
         pass

#--------------------------------------

class Camera_box(Sprite_surface):
   def __init__(self, ID, x, y, sprite=None, coll_boxes=None):
      super().__init__(ID, x, y, sprite, coll_boxes)