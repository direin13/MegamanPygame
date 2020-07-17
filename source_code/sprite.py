#!/usr/bin/env python
import pygame
from mega_stack import *
import timer
import os

class Sprite(object):
   """Base class for making sprite animations"""

   def __init__(self, ID, x, y, width, height, active_frames, change_rgb_value=False, rgb=(10,10,10,0)):
      """Initialise a sprite. ID is a string.
         active_framea is a list of tuples containing animations
         e.g [(animation_name, [loaded_images], int_animation_speed)]"""
      self.ID = ID
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.active_frames = active_frames
      self.all_frames = {}
      self.all_frame_speed = {}
      self.all_timers = timer.Timer()

      if change_rgb_value:
         self.change_sprite_rgb_value(rgb)

      for t in self.active_frames:
         self.all_frames[t[0]] = t[1]
         self.all_frame_speed[t[0]] = t[2]

      self.current_frame = 0
      self.current_animation = self.active_frames[0][0]
      self.all_timers.add_ID('time_till_next_frame', 0)


   @staticmethod
   def load_images(directory):
      directory_images = {}

      for image in os.listdir(directory):
         try:
            directory_images[image.split('.')[0]] = pygame.image.load('{}/{}'.format(directory, image))
         except:
            pass

      return directory_images
         #--the name of the file(without the file extension) return to the loaded image itself e.g all_images[name] will return the loaded image of name.png--


   def get_frames(self, frame_name):
      """return the original list of surfaces that make up the animation"""
      return self.all_frames[frame_name]


   def change_sprite_rgb_value(self, rgb):
      for t in self.active_frames:
         new_imgs = [img.copy() for img in t[1]]

         for img in new_imgs:
            new_surf = pygame.Surface((img.get_width(), img.get_height()), flags=pygame.SRCALPHA)
            new_surf.fill(rgb)
            img.blit(new_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

         for i in range(len(new_imgs)):
            t[1][i] = new_imgs[i]
            

   def get_frame_speed(self, frame_name):
      """returns the number of total frames given to play specified animation"""
      return self.all_frame_speed[frame_name]


   def display_animation(self, surf, frame_name, x_offset=0, y_offset=0, flip=False, resume=False):
      """displays animations from 'frame_name' in self.active_frames"""
      if self.active_frames != None:
         if self.current_animation == frame_name or resume == True and self.current_frame <= len(self.get_frames(frame_name)):
            self.current_animation = frame_name 
            pass
         else:
            self.current_animation = frame_name 
            self.current_frame = 0
            self.all_timers.get_loop_states('time_till_next_frame')['curr_state'] = 1
            
         image = self.get_frames(frame_name)[self.current_frame]
         frame = pygame.transform.scale(image, (self.width, self.height))

         if flip == True:
            frame = pygame.transform.flip(frame, True, False)

         surf.blit(frame, (self.x + x_offset, self.y + y_offset))


   def update(self, auto_reset=True, loop_amount=-1):
      """used to cycle through the current animation list of the sprite.
         should be used once per frame, per animation."""
      if self.active_frames != None:
         frame_speed = self.all_frame_speed[self.current_animation]
         number_of_frames = len(self.all_frames[self.current_animation])
         frame_per_update = frame_speed // number_of_frames

         if loop_amount == -1: #loop forever
            self.all_timers.countdown('time_till_next_frame', frame_per_update, loop=True)
         else:
            self.all_timers.countdown('time_till_next_frame', frame_per_update, loop=True, loop_amount=loop_amount*number_of_frames)

         if self.all_timers.is_finished('time_till_next_frame'):
            self.current_frame += 1

         if self.current_frame >= number_of_frames:
            if auto_reset == True:
               self.current_frame = 0
            else:
               if self.all_timers.is_finished('time_till_next_frame', include_loop=True):
                  self.current_frame = number_of_frames - 1
               else:
                  self.current_frame = 0

#--------------------------------------------------------------------

class Collision_box(object):

   def __init__(self, ID, x, y, width, height, colour=(255,0,0), x_offset=0, y_offset=0):
      #--In pygame, a surface's x and y co_ordinate starts from the top left corner which I felt was inconvenient for collision boxes, so here the x and y starts at the middle of the box

      self.ID = ID
      self.is_active = True
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



   def collision(self, other):
      return self.box_collision(other) or other.box_collision(self)

#---------------------------------------------------

class Sprite_surface(object):
   """base class for objects that have a set of sprite(s) and set of of collision box(es) attached to it"""
   all_sprite_surfaces = []
   all_name_count = {}
   display_screen = None

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=1, display_offset=[0,0]):
      Sprite_surface.add_to_class_lst(self, Sprite_surface.all_sprite_surfaces, ID)
      self.display_offset = display_offset
      self.ID = ID
      self.spawn_point = [x, y]
      self.x = x
      self.y = y
      self.is_active = is_active
      self.width = width
      self.height = height
      self.display_layer = display_layer
      self.collbox_dict = {}
      self.sprite_dict = {}
      if coll_boxes != None:
         for coll_box in coll_boxes: #adding all the coll boxes and sprites to respective dictionaries
            self.collbox_dict[coll_box.ID] = coll_box

      if sprites == None:
         self.sprite_dict = None
      else:
         for sprite in sprites:
            self.sprite_dict[sprite.ID] = sprite

   @classmethod
   def add_to_class_lst(cls, self, lst, ID):
      """will add self to specified lst"""

      if cls == Sprite_surface:
         if ID in Sprite_surface.all_name_count: #--trying add sprite surface while avoiding duplicates
            Sprite_surface.all_name_count[ID] += 1
            self.reference_ID = '{}-{}'.format(ID, Sprite_surface.all_name_count[ID]) #--if ID is in all_sprite_surfaces the count will increment and be attached to the reference ID
         else:
            Sprite_surface.all_name_count[ID] = 0
            self.reference_ID = '{}-{}'.format(ID, Sprite_surface.all_name_count[ID])
      lst.append(self)


   def display_collboxes(self, surf, alpha=100):
      #displays all of selfs collision boxes
      for collbox in self.collbox_dict.values():
         collbox.display_collbox(surf, alpha)


   def get_collbox(self, coll_box):
      return self.collbox_dict[coll_box]


   def collision(self, other, coll_box_self, coll_box_other):
      return self.get_collbox(coll_box_self).collision(other.get_collbox(coll_box_other))

   def check_collision_lst(self, lst, coll_box_self, coll_box_other, quota=None):
      """will check collision between 2 boxes with every sprite_surface in the lst
         if quota = n, then function will return break and true when n collisions are found, if quota = None, every element in list will be check"""
      all_collisions = Stack()
      i = 0
      quota_reached = False
      while  i < len(lst) and quota_reached == False:
         sprite_surf = lst[i]
         if (sprite_surf != self and sprite_surf.is_active == True 
            and self.collision(sprite_surf, coll_box_self, coll_box_other) == True):

            all_collisions.push(sprite_surf)
            if quota != None:
               quota -= 1
               if quota <= 0:
                  quota_reached = True
         i += 1

      return all_collisions



   def update_sprite(self, sprite, auto_reset=True, loop_amount=-1):
      """calls update from Sprite class"""
      sprite = self.get_sprite(sprite)
      sprite.update(auto_reset, loop_amount)

   def display_animation(self, sprite_obj_ID, surf, frame_name, x_offset=0, y_offset=0, flip=False, resume=False):
      """calls display_animation from Sprite class"""
      self.get_sprite(sprite_obj_ID).display_animation(surf, frame_name, x_offset + self.display_offset[0], y_offset + self.display_offset[1], flip, resume)

   def set_animation(self, sprite_obj_ID, frame_name, resume=False):
      """calls set_animation from Sprite class"""
      sprite = self.get_sprite(sprite_obj_ID)
      sprite.set_animation(frame_name, resume)


   def get_sprite(self, sprite_obj, row=None):
      """returns specified sprite in sprite_dict, if row is specified then 
         sprite.active_frames[row] will be returned"""

      if row == None:
         return self.sprite_dict[sprite_obj]
      else:
         return self.sprite_dict[sprite_obj].active_frames[row]


   def update(self): 
      """Makes sure all attached collision boxes and sprite images follow the sprite_surface"""
      if len(self.collbox_dict) != 0:
         for coll_box in self.collbox_dict.values():
            coll_box.x = self.x + (coll_box.width // 2) + coll_box.x_offset
            coll_box.y = self.y + (coll_box.height // 2) + coll_box.y_offset
            coll_box.left_edge = coll_box.x - (coll_box.width // 2)
            coll_box.right_edge = coll_box.x + (coll_box.width // 2)
            coll_box.top_edge = coll_box.y - (coll_box.height // 2)
            coll_box.bottom_edge = coll_box.y + (coll_box.height // 2)

      if self.sprite_dict != None:
         for sprite in self.sprite_dict.values():
            sprite.x = self.x
            sprite.y = self.y


   def is_on_screen(self, x_clip_offset=0, y_clip_offset=0):
      screen_width, screen_height = Sprite_surface.display_screen.get_size()
      if ((self.x < screen_width + x_clip_offset and self.x + self.width > -x_clip_offset) and
         (self.y < screen_height + y_clip_offset and self.y + self.height > -y_clip_offset)):
         return True
      else:
         return False
      
#----------------------------------------------------------------