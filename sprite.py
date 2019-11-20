#!/usr/bin/env python
import pygame
from mega_stack import *
import timer
import os

class Sprite(object):

   def __init__(self, ID, x, y, width, height, active_frames=None, current_frame=0):
      self.ID = ID
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      #--make sure the active frames are in the order you want in a list--
      #--active_frames should contain a list of tuples. For each tuple, tuple[0] is the string name of the set of animations and tuple[1] are the images themselves, tuple[3] is the speed at which the set of frames should be played--
      #--e.g active_frame = [('random_animation_1', [picture_1, picture_2, picture_3]), ('random_animation_2', [picture_4])]
      self.active_frames = active_frames
      self.all_frames = {}
      self.all_frame_speed = {}

      if active_frames != None:
         for t in self.active_frames:
            self.all_frames[t[0]] = t[1]
            self.all_frame_speed[t[0]] = t[2]

         self.current_frame = current_frame
         self.current_animation = self.active_frames[0][0]
         self.flag = 0
      self.all_timers = timer.Timer()

   def get_frames(self, frame_name):
      return self.all_frames[frame_name]

   def get_frame_speed(self, frame_name):
      return self.all_frame_speed[frame_name]

   def display_animation(self, surf, frame_name, x_offset=0, y_offset=0, flip=False):
      #--displays animations from 'frame name' in self.active_frames--
      if self.active_frames != None:
         if self.current_animation == frame_name:
            pass
         else:
            self.current_animation = frame_name 
            self.current_frame = 0

         frame = pygame.transform.scale(self.get_frames(frame_name)[self.current_frame], (self.width, self.height))
         if flip == True:
            frame = pygame.transform.flip(frame, True, False)
         surf.blit(frame, (self.x + x_offset, self.y + y_offset))
      else:
         print('you need "active_frames" to use display_animation()')

   def update(self, frame_speed):
      #--used to cycle through the sprite's animations
      if self.active_frames != None:
         frame_per_update = frame_speed // len(self.all_frames[self.current_animation])

         if self.all_timers.countdown('update_flag', frame_per_update, loop=True) == False:
            self.current_frame += 1

         if self.current_frame >= len(self.all_frames[self.current_animation]):
            self.current_frame = 0
      else:
         print('you need "active_frames" to use update()')

#--------------------------------------------------------------------

class Collision_box(object):

   def __init__(self, ID, x, y, width, height, colour=(255,0,0), x_offset=0, y_offset=0):
      #--In pygame, a surface's x and y co_ordinate starts from the top left corner which I felt was inconvenient for collision boxes, so here the x and y starts at the middle of the box

      self.ID = ID
      self.x_offset = x_offset
      self.y_offset = y_offset
      self.x = x + (width // 2) + self.x_offset
      self.y = y + (height // 2) + self.y_offset
      self.width = width
      self.height = height
      self.colour = colour
      self.left_edge = self.x - (width // 2)
      self.right_edge = self.x + (width // 2)
      self.top_edge = self.y - (height // 2)
      self.bottom_edge = self.y + (height // 2)
      self.box = pygame.Surface((self.width, self.height))



   def display_collbox(self, surf, alpha=100):
      self.box.set_alpha(alpha)
      self.box.fill(self.colour)
      surf.blit(self.box, (self.x - (self.width//2), self.y - (self.height//2)))
      pygame.draw.circle(surf, (0, 0, 0), (self.left_edge, self.y), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.right_edge, self.y), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.x, self.top_edge), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.x, self.bottom_edge), 2)
      pygame.draw.circle(surf, (0, 0, 0), (self.x, self.y), 2)


   def box_collision(self, other):
      #--this checks if another Collison_box object is colliding with the self and returns True or False--
      if ((self.right_edge <= other.right_edge and self.right_edge >= other.left_edge) or 
          (self.left_edge >= other.left_edge and self.left_edge <= other.right_edge)):

         if ((self.top_edge >= other.top_edge and self.top_edge <= other.bottom_edge) or 
            (self.bottom_edge <= other.bottom_edge and self.bottom_edge >= other.top_edge)):
            return True
         elif (other.x > self.left_edge and other.x < self.right_edge and 
              other.y > self.top_edge and other.y < self.bottom_edge):
            return True

      elif (other.x > self.left_edge and other.x < self.right_edge and 
           other.y > self.top_edge and other.y < self.bottom_edge):
         return True



   def collision_sprite(self, other):
      return self.box_collision(other) or other.box_collision(self)

#---------------------------------------------------

class Sprite_surface(object):
   #--this is an object that has a sprite and set of of collision boxes attached to it
   all_sprite_surfaces = {}
   all_name_index = {}

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=1):
      Sprite_surface.add_to_class_dict(self, ID)
      self.ID = ID
      self.x = x
      self.y = y
      self.sprites = sprites
      self.coll_boxes = coll_boxes
      self.collbox_dict = {}
      self.sprite_dict = {}
      self.is_active = is_active
      self.width = width
      self.height = height
      self.display_layer = display_layer
      if coll_boxes == None:
            pass
      else:
         for coll_box in coll_boxes:
            self.collbox_dict[coll_box.ID] = coll_box

      if sprites == None:
         pass
      else:
         for sprite in sprites:
            self.sprite_dict[sprite.ID] = sprite

   @classmethod
   def add_to_class_dict(cls, self, ID):
      #will add self to specified dictionary

      if cls == Sprite_surface:
         if ID in Sprite_surface.all_name_index: #--trying add sprite surface while avoiding duplicates
            Sprite_surface.all_name_index[ID] += 1
            self.reference_ID = '{}-{}'.format(ID, Sprite_surface.all_name_index[ID]) #--if ID is in all_sprite_surfaces the Index will increment and be attached to the reference ID
         else:
            Sprite_surface.all_name_index[ID] = 0
            self.reference_ID = '{}-{}'.format(ID, Sprite_surface.all_name_index[ID])
      cls.all_sprite_surfaces[self.reference_ID] = self

   def assert_ID(self):
      return self.reference_ID in Sprite_surface.all_sprite_surfaces


   def add_collbox(self, ID, x, y, width, height, x_offset=0, y_offset=0):
      box = Collision_box(ID, x, y, width, height, x_offset, y_offset)
      self.collbox_dict[box.ID] = box
      self.coll_boxes.append(box)

   def display_collboxes(self, surf, alpha=100):
      #displays all of selfs collision boxes
      for collbox in self.collbox_dict.values():
         collbox.display_collbox(surf, alpha)


   def get_collbox(self, coll_box):
      return self.collbox_dict[coll_box]


   def check_collision(self, other, coll_box_self, coll_box_other):
      return self.get_collbox(coll_box_self).collision_sprite(other.get_collbox(coll_box_other))

   def check_collision_dict(self, dictionary, coll_box_self, coll_box_other, quota=None):
      #will check specified collision with every element in the dictionary
      #if quota = n, then function will return true when n collisions are found and break, if quota = None, every sprite_surf will be check
      all_collisions = Stack()
      for sprite_surf in dictionary.values():
         if sprite_surf != self and sprite_surf.is_active == True and self.check_collision(sprite_surf, coll_box_self, coll_box_other) == True:
            all_collisions.push(sprite_surf)
            if quota == None:
               pass
            else:
               quota -= 1
               if quota <= 0:
                  break

      return all_collisions


   def add_sprite(self, ID, x, y, width, height, active_frames=None, current_frame=0):
      sprite = Sprite(ID, x, y, width, height, active_frames, current_frame)
      self.sprite_dict[ID] = sprite
      self.sprites.append(sprite)


   def update_sprite(self, sprite):
      sprite = self.get_sprite(sprite)
      frame_speed = sprite.get_frame_speed(sprite.current_animation)
      sprite.update(frame_speed)

   def display_animation(self, sprite, surf, frame_name, x_offset=0, y_offset=0, flip=False):
      self.get_sprite(sprite).display_animation(surf, frame_name, x_offset, y_offset, flip)


   def get_sprite(self, sprite, row=None):
      #returns specified sprite group, if row is specified then self.active_frames will be searched by index
      if row == None:
         return self.sprite_dict[sprite]
      else:
         return self.sprite_dict[sprite].active_frames[row]


   def update(self):
      try:
         for coll_box in self.collbox_dict.values():
            coll_box.x = self.x + (coll_box.width // 2) + coll_box.x_offset
            coll_box.y = self.y + (coll_box.height // 2) + coll_box.y_offset
            coll_box.left_edge = coll_box.x - (coll_box.width // 2)
            coll_box.right_edge = coll_box.x + (coll_box.width // 2)
            coll_box.top_edge = coll_box.y - (coll_box.height // 2)
            coll_box.bottom_edge = coll_box.y + (coll_box.height // 2)
      except ValueError:
         pass
      try:
         for sprite in self.sprite_dict.values():
            sprite.x = self.x
            sprite.y = self.y
      except AttributeError:
         pass


   def is_on_screen(self, screen_width, screen_height):
      #checks if sprite_surf is on the screen
      if ((self.x < screen_width -10 and self.x + self.width > 10) and 
         (self.y < screen_height -10 and self.y + self.height > 10)):
         return True
      else:
         return False
      
#----------------------------------------------------------------

class Camera(object):
   def __init__(self, x, y, static=True):
      self.x = x
      self.y = y
      self.static = static
      self.all_timers = timer.Timer()

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
               if self.get_pos_x(main_sprite_surf) == 0:
                  sprite_surf.x += speed
               if self.get_pos_x(main_sprite_surf) == 1:
                  sprite_surf.x -= speed
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

   def move(self, direction, speed):
      x = 0
      y = 0
      if direction == 'right':
         x = -speed
      if direction == 'up':
         y = speed
      if direction == 'left':
         x = speed
      if direction == 'down':
         y = -speed
      for sprite_surf in Sprite_surface.all_sprite_surfaces.values():
         sprite_surf.x += x
         sprite_surf.y += y

   def transition(self, direction, speed, lenght):
      if self.all_timers.countdown('transition_flag', lenght) == True:
         self.move(direction, speed)



#--------------------------------------

class Camera_box(Sprite_surface):
   all_sprite_surfaces = {}
   
   def __init__(self, ID, x, y, sprite=None, coll_boxes=None, display_layer=1):
      super().__init__(ID, x, y, sprite, coll_boxes, display_layer)
      Camera_box.add_to_class_dict(self, ID)