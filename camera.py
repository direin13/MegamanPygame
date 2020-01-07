#!usr/bin/env python
from sprite import *
import universal_names
import timer
import bar

class Camera(object):
   def __init__(self, x, y, sprite_surf=None):
      self.x = x
      self.y = y
      self.x_vel = 1
      self.y_vel = 1
      self.all_timers = timer.Timer()
      self.all_timers.add_ID('x_static', 2)
      self.sprite_surf = sprite_surf
      self.is_active = True

   def follow(self, sprite_surf, x=True, y=False):
      self.is_active = True
      self.sprite_surf = sprite_surf
      xdist = self.x - self.sprite_surf.x

      if self.sprite_surf.x_vel == 0:
         self.all_timers.replenish_timer('x_static')
      else:
         self.all_timers.countdown('x_static')


      for obj in Sprite_surface.all_sprite_surfaces:
         if x == True and xdist != 0 and self.all_timers.is_empty('x_static') and isinstance(obj, bar.Bar) != True:
            obj.x += xdist
            if obj != self.sprite_surf:
               obj.spawn_point[0] += xdist
      if x == True and xdist != 0 and self.all_timers.is_empty('x_static'):
         universal_names.world_location[0] -= xdist



   def move(self, speed, direction):
      x = 0
      y = 0
      if direction == 'right':
         self.x -= speed
         x -= speed
      if direction == 'left':
         self.x += speed
         x += speed
      if direction == 'down':
         self.y -= speed
         y -= speed
      if direction == 'up':
         self.y += speed
         y += speed

      for obj in Sprite_surface.all_sprite_surfaces:
         if isinstance(obj, bar.Bar) != True:
            obj.x += x
            obj.y += y
            if obj != self.sprite_surf:
               obj.spawn_point[0] += x
               obj.spawn_point[1] += y
      universal_names.world_location[0] -= x
      universal_names.world_location[1] -= y

   def update_position(self):
      if self.is_active != True:
         self.x, self.y = universal_names.camera_x, universal_names.camera_y

      self.is_active = False
#--------------------------------------

class Camera_box(Sprite_surface):
   all_camera_box = []
   
   def __init__(self, ID, x, y, width, height, display_layer=1):
      coll_boxes = [Collision_box(universal_names.hitbox, 300, 400, width, height)]
      super().__init__(ID, x, y, None, coll_boxes, display_layer)
      Camera_box.add_to_class_lst(self, Camera_box.all_camera_box, ID)

#------------------------------------------------------------------------------------------

class Transition_box(Sprite_surface): #Use to transition the full screen in a direction
   all_transition_box = []
   all_timers = timer.Timer()
   all_timers.add_ID('transition_start', 30)
   all_timers.add_ID('transition_end', 40)
   in_transition_mode = False #If the screen is currently in transition
   current_box = None #Whichever box activated the transition
   transition_speed = 10
   
   def __init__(self, ID, x, y, display_layer=1, direction='left', size=200):
      if direction == 'left' or direction == 'right':
         width = 10
         height = size
      else:
         width = size
         height = 10

      coll_boxes = [Collision_box(universal_names.hitbox, 300, 400, width, height, colour=(200, 255, 100))]
      super().__init__(ID, x, y, None, coll_boxes, display_layer)
      Transition_box.add_to_class_lst(self, Transition_box.all_transition_box, ID)
      self.all_timers = timer.Timer()
      self.original_direction = direction
      self.direction = direction
      if direction == 'left' or direction == 'right':
         Transition_box.all_timers.add_ID(ID, universal_names.screen_width) #Timer for how long the transition should be
      else:
         Transition_box.all_timers.add_ID(ID, universal_names.screen_height)

   def switch_dir(self):
      if self.direction == 'left':
         self.direction = 'right'

      elif self.direction == 'right':
         self.direction = 'left'

      elif self.direction == 'up':
         self.direction = 'down'

      else:
         self.direction = 'up'


#-------------------------------------------------------------


#--Functions--

def check_camerabox_collision(sprite_surf):
   collisions = sprite_surf.check_collision_lst(Camera_box.all_camera_box, universal_names.hitbox, universal_names.hitbox, quota=1)
   return collisions.is_empty() != True



def check_transitionbox_collision(sprite_surf):
   collisions = sprite_surf.check_collision_lst(Transition_box.all_transition_box, universal_names.hitbox, universal_names.hitbox, quota=1) #returns stack of 1 collision
   if collisions.is_empty() != True and Transition_box.in_transition_mode != True:
      tbox = collisions.pop()
      Transition_box.current_box = tbox
      Transition_box.in_transition_mode = True
      Transition_box.all_timers.replenish_timer(tbox.ID)


      
def transition_screen(camera):
   tbox = Transition_box.current_box
   if Transition_box.all_timers.is_empty('transition_start') != True:
      Transition_box.all_timers.countdown('transition_start') #Wait for a little pause before transitioning
      universal_names.game_pause = True

   else:
      if Transition_box.all_timers.is_empty(tbox.ID) != True: #If timer is not empty keep transitioning
         universal_names.game_pause = False
         camera.move(Transition_box.transition_speed, tbox.direction)

         if tbox.direction == 'right':  #move megaman
            camera.sprite_surf.follow(x=tbox.collbox_dict[universal_names.hitbox].x, x_vel=2)
         elif tbox.direction == 'left':
            camera.sprite_surf.follow(x=(tbox.collbox_dict[universal_names.hitbox].x - camera.sprite_surf.width), x_vel=2)
         elif tbox.direction == 'up':
            camera.sprite_surf.follow(y=(tbox.collbox_dict[universal_names.hitbox].y - camera.sprite_surf.height), y_vel=2)
         else:
            camera.sprite_surf.follow(y=tbox.collbox_dict[universal_names.hitbox].y + 25, y_vel=2)

         Transition_box.all_timers.countdown(tbox.ID, countdown_speed=Transition_box.transition_speed)
      else:
         if Transition_box.all_timers.is_empty('transition_end') != True:
            Transition_box.all_timers.countdown('transition_end') #wait for a little pause again before finishing transition
            universal_names.game_pause = True
         else:
            universal_names.game_pause = False
            Transition_box.in_transition_mode = False
            tbox.switch_dir()
            Transition_box.all_timers.replenish_timer('transition_start')
            Transition_box.all_timers.replenish_timer('transition_end')


def update(camera):
   if check_camerabox_collision(camera.sprite_surf) != True and Transition_box.in_transition_mode != True and camera.sprite_surf.is_active:
      camera.follow(camera.sprite_surf)
   check_transitionbox_collision(camera.sprite_surf)
   if Transition_box.current_box != None and Transition_box.in_transition_mode == True:
      transition_screen(camera)
   camera.update_position()


def camera_transitioning():
   return Transition_box.in_transition_mode

def transition_start_end(): #returns true if transition phase is at the begining or end points
   if camera_transitioning():
      return Transition_box.all_timers.is_empty('transition_start') != True or Transition_box.all_timers.is_empty(Transition_box.current_box.ID)
   else:
      return False