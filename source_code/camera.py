#!usr/bin/env python
from sprite import *
import universal_var
import timer
import bar
import projectile

class World_camera(object):
   world_location = [0, 0] #player position from the origin
   original_position = [250, 200]
   x = original_position[0]
   y = original_position[1]
   x_offset = 0
   y_offset = 0
   all_timers = timer.Timer()
   all_timers.add_ID('camera_shake_interval', 0)
   target_focus = None
   static = False

   @classmethod
   def follow(cls, sprite_surf=None):
      if sprite_surf == None:
         cls.static = True
      else:
         cls.target_focus = sprite_surf

      if cls.static:
         xdist = 0
         ydist = 0
      else:
         xdist = cls.x - cls.target_focus.x
         ydist = cls.y - cls.target_focus.y

      for obj in Sprite_surface.all_sprite_surfaces:
         if isinstance(obj, bar.Energy_bar) != True:
            obj.x += xdist
            obj.display_offset = [cls.x_offset, cls.y_offset]
            if obj.ID != 'megaman':
               obj.spawn_point[0] += xdist

            if isinstance(obj, projectile.Projectile):
               obj.init_x += xdist
            Sprite_surface.update(obj)

      if universal_var.debug == True:
         for obj in Sprite_surface.all_sprite_surfaces:
            if isinstance(obj, bar.Energy_bar) != True:
               obj.y += ydist
               if obj.ID != 'megaman':
                  obj.spawn_point[1] += ydist
               if isinstance(obj, projectile.Projectile):
                  obj.init_y += ydist
               Sprite_surface.update(obj)
      
      cls.world_location[0] -= xdist
      if universal_var.debug == True:
         cls.world_location[1] -= ydist


   @classmethod
   def move(cls, speed, direction):
      x = 0
      y = 0
      if direction == 'right':
         cls.x -= speed
         x -= speed
      if direction == 'left':
         cls.x += speed
         x += speed
      if direction == 'down':
         cls.y -= speed
         y -= speed
      if direction == 'up':
         cls.y += speed
         y += speed

      for obj in Sprite_surface.all_sprite_surfaces:
         if isinstance(obj, bar.Energy_bar) != True:
            obj.x += x
            obj.y += y
            if obj != cls.target_focus:
               obj.spawn_point[0] += x
               obj.spawn_point[1] += y
            if isinstance(obj, projectile.Projectile):
               obj.init_x += x
               obj.init_y += y
      cls.world_location[0] -= x
      cls.world_location[1] -= y


   @classmethod
   def shake(cls, x_offset, y_offset, speed=5):
      half_way_time = cls.all_timers.get_ID('camera_shake_interval')['origin']//2
      if cls.all_timers.is_almost_finished('camera_shake_interval', half_way_time):
         cls.x_offset = x_offset
         cls.y_offset = y_offset
      else:
         cls.x_offset = -x_offset
         cls.y_offset = -y_offset

      cls.all_timers.countdown('camera_shake_interval', speed, loop=True)

   @classmethod
   def update(cls):
      if cls.target_focus != None and universal_var.debug != True and universal_var.hitbox in cls.target_focus.collbox_dict:
         if check_camerabox_collision(cls.target_focus) != True and Transition_box.in_transition_mode != True and cls.target_focus.is_active:
            cls.static = False
         elif check_camerabox_collision(cls.target_focus) or Transition_box.in_transition_mode:
            cls.static = True

         cls.follow(cls.target_focus)


         if universal_var.game_reset != True:
            check_transitionbox_collision(cls.target_focus)
            if Transition_box.current_box != None and Transition_box.in_transition_mode == True:
               transition_screen()

      elif universal_var.debug:
         cls.static = False
         cls.follow(cls.target_focus)

      else:
         cls.static = True
         cls.follow()
               
      #reset position
      cls.x, cls.y = cls.original_position[0], cls.original_position[1]
      cls.x_offset, cls.y_offset = 0, 0
#--------------------------------------

class Camera_box(Sprite_surface):
   all_camera_box = []
   
   def __init__(self, ID, x, y, width, height, display_layer=1, colour=(62, 48, 255)):
      coll_boxes = [Collision_box(universal_var.hitbox, 300, 400, width, height, colour=colour)]
      super().__init__(ID, x, y, None, coll_boxes, display_layer)
      Camera_box.add_to_class_lst(self, Camera_box.all_camera_box, ID)

#------------------------------------------------------------------------------------------

class Transition_box(Sprite_surface): #Use to transition the full screen in a direction
   all_transition_box = []
   all_timers = timer.Timer()
   all_timers.add_ID('transition_start', 20)
   all_timers.add_ID('transition_end', 20)
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

      coll_boxes = [Collision_box(universal_var.hitbox, 300, 400, width, height, colour=(200, 255, 100))]
      super().__init__(ID, x, y, None, coll_boxes, display_layer)
      Transition_box.add_to_class_lst(self, Transition_box.all_transition_box, ID)
      self.all_timers = timer.Timer()
      self.original_direction = direction
      self.direction = direction
      if direction == 'left' or direction == 'right':
         Transition_box.all_timers.add_ID(ID, universal_var.screen_width) #Timer for how long the transition should be
      else:
         Transition_box.all_timers.add_ID(ID, universal_var.screen_height)

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
   collisions = sprite_surf.check_collision_lst(Camera_box.all_camera_box, universal_var.hitbox, universal_var.hitbox, quota=1)
   return collisions.is_empty() != True



def check_transitionbox_collision(sprite_surf):
   collisions = sprite_surf.check_collision_lst(Transition_box.all_transition_box, universal_var.hitbox, universal_var.hitbox, quota=1) #returns stack of 1 collision
   if collisions.is_empty() != True and Transition_box.in_transition_mode != True:
      tbox = collisions.pop()
      Transition_box.current_box = tbox
      Transition_box.in_transition_mode = True
      Transition_box.all_timers.replenish_timer(tbox.ID)


      
def transition_screen():
   tbox = Transition_box.current_box
   if Transition_box.all_timers.is_finished('transition_start') != True:
      Transition_box.all_timers.countdown('transition_start') #Wait for a little pause before transitioning
      universal_var.game_pause = True

   else:
      if Transition_box.all_timers.is_finished(tbox.ID) != True: #If timer is not empty keep transitioning
         universal_var.game_pause = False
         World_camera.move(Transition_box.transition_speed, tbox.direction)

         sprite_surf = World_camera.target_focus
         if tbox.direction == 'right':  #move megaman
            sprite_surf.follow(x=tbox.collbox_dict[universal_var.hitbox].x + 30, x_vel=2)
         elif tbox.direction == 'left':
            sprite_surf.follow(x=(tbox.collbox_dict[universal_var.hitbox].x - World_camera.target_focus.width - 30), x_vel=2)
         elif tbox.direction == 'up':
            sprite_surf.follow(y=(tbox.collbox_dict[universal_var.hitbox].y - World_camera.target_focus.height), y_vel=2)
         else:
            sprite_surf.follow(y=tbox.collbox_dict[universal_var.hitbox].y + 25, y_vel=2)

         Transition_box.all_timers.countdown(tbox.ID, countdown_speed=Transition_box.transition_speed)
      else:
         if Transition_box.all_timers.is_finished('transition_end') != True:
            Transition_box.all_timers.countdown('transition_end') #wait for a little pause again before finishing transition
            universal_var.game_pause = True
         else:
            universal_var.game_pause = False
            Transition_box.in_transition_mode = False
            tbox.switch_dir()
            Transition_box.all_timers.replenish_timer('transition_start')
            Transition_box.all_timers.replenish_timer('transition_end')


def camera_transitioning():
   return Transition_box.in_transition_mode

def transition_start(): #returns true if transition phase is at the begining
   if camera_transitioning():
      return Transition_box.all_timers.is_finished('transition_start') != True
   else:
      return False

def transition_end():
   if camera_transitioning():
      return Transition_box.all_timers.is_finished(Transition_box.current_box.ID)
   else:
      return False