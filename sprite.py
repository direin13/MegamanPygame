#!/usr/bin/env python
import pygame
from mega_stack import *
import timer

class Sprite(object):

   def __init__(self, ID, x, y, width, height, active_frames, current_frame=0, change_rgb_value=False, rgb=(10,10,10,0)):
      self.ID = ID
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      #--make sure the active frames are in the order you want in a list--
      #--active_frames should contain a list of tuples. For each tuple, tuple[0] is the string name of the set of animations and tuple[1] are the images themselves, tuple[2] is the speed at which the set of frames should be played--
      #--e.g active_frame = [('random_animation_1', [picture_1, picture_2, picture_3], some_speed), ('random_animation_2', [picture_4], some_other_speed)]
      self.active_frames = active_frames
      self.all_frames = {}
      self.all_frame_speed = {}
      self.all_timers = timer.Timer()

      if change_rgb_value:
         self.change_sprite_rgb_value(rgb)

      for t in self.active_frames:
         self.all_frames[t[0]] = t[1]
         self.all_frame_speed[t[0]] = t[2]

      self.current_frame = current_frame
      self.current_animation = self.active_frames[0][0]


   def get_frames(self, frame_name):
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
      return self.all_frame_speed[frame_name]

   def display_animation(self, surf, frame_name, x_offset=0, y_offset=0, flip=False, resume=False):
      #--displays animations from 'frame name' in self.active_frames--
      if self.active_frames != None:
         if self.current_animation == frame_name or resume == True:
            self.current_animation = frame_name 
            pass
         else:
            self.current_animation = frame_name 
            self.current_frame = 0

         image = self.get_frames(frame_name)[self.current_frame]
         frame = pygame.transform.scale(image, (self.width, self.height))

         if flip == True:
            frame = pygame.transform.flip(frame, True, False)
         surf.blit(frame, (self.x + x_offset, self.y + y_offset))

   def update(self, auto_reset=True):
      #--used to cycle through the sprite's animations
      if self.active_frames != None:
         frame_speed = self.all_frame_speed[self.current_animation]
         frame_per_update = frame_speed // len(self.all_frames[self.current_animation])
         self.all_timers.countdown('update_flag', frame_per_update, loop=True)

         if self.all_timers.is_empty('update_flag'):
            self.current_frame += 1

         if self.current_frame >= len(self.all_frames[self.current_animation]):
            if auto_reset == True:
               self.current_frame = 0
            else:
               self.current_frame = len(self.all_frames[self.current_animation]) - 1

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
   #--this is an object that has a set of sprite and set of of collision boxes attached to it
   all_sprite_surfaces = []
   all_name_count = {}

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=1):
      Sprite_surface.add_to_class_lst(self, Sprite_surface.all_sprite_surfaces, ID)
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
      #will add self to specified lst

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
      #will check specified collision with every sprite_surface in the lst
      #if quota = n, then function will return break and true when n collisions are found, if quota = None, every element in list will be check
      all_collisions = Stack()
      for sprite_surf in lst:
         if (sprite_surf != self and sprite_surf.is_active == True 
            and self.collision(sprite_surf, coll_box_self, coll_box_other) == True):

            all_collisions.push(sprite_surf)
            if quota == None:
               pass
            else:
               quota -= 1
               if quota <= 0:
                  break

      return all_collisions



   def update_sprite(self, sprite, auto_reset=True): # Use to move onto next sprite frame
      sprite = self.get_sprite(sprite)
      sprite.update(auto_reset)

   def display_animation(self, sprite_obj_ID, surf, frame_name, x_offset=0, y_offset=0, flip=False, resume=False):
      self.get_sprite(sprite_obj_ID).display_animation(surf, frame_name, x_offset, y_offset, flip, resume)

   def set_animation(self, sprite_obj_ID, frame_name, resume=False):
      sprite = self.get_sprite(sprite_obj_ID)
      sprite.set_animation(frame_name, resume)


   def get_sprite(self, sprite_obj, row=None):
      #returns specified sprite group, if row is specified then self.active_frames will be searched by index

      if row == None: #row is specified row in list of all frames
         return self.sprite_dict[sprite_obj]
      else:
         return self.sprite_dict[sprite_obj].active_frames[row]


   def update(self): #Makes sure all attached collision boxes and sprite images follow the sprite_surface
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


   def is_on_screen(self, screen_width, screen_height, x_clip_offset=0, y_clip_offset=0):
      if ((self.x < screen_width + x_clip_offset and self.x + self.width > -x_clip_offset) and
         (self.y < screen_height + y_clip_offset and self.y + self.height > -y_clip_offset)):
         return True
      else:
         return False
      
#----------------------------------------------------------------