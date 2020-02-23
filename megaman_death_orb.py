#!/usr/bin/env python
import pygame
from sprite import *
from megaman_object import *
import universal_var
import timer
import projectile

all_orbs = []
orb = {}
orb_timers = timer.Timer()
spawned = True


def init(sprite_surf):
   global all_orbs
   global orb_timers

   orb_animation = [universal_var.effect_images['death_orb_1'], universal_var.effect_images['death_orb_2'], universal_var.effect_images['death_orb_3'],
              universal_var.effect_images['death_orb_4']]
   for i in range(0, 12):
      orb_sprite = Sprite(universal_var.main_sprite, 200, 200, 40, 40, [('orb', orb_animation, 20)])
      orb = Megaman_object('orb', sprite_surf.x, sprite_surf.y, sprites=[orb_sprite], width=40, height=40, display_layer=4, is_active=False)
      all_orbs.append(orb)
   orb_timers.add_ID('wave_1', 30)
   orb_timers.add_ID('wave_2', 60)



def spawn_orbs(sprite_surf):
   global spawned

   if spawned == True:
      for orb in all_orbs:
         orb.teleport(sprite_surf.x + 25, sprite_surf.y + 22)
   spawned = False



def set_orb_active():
   global all_orbs

   for orb in all_orbs:
      orb.is_active = True


def reset():
   global all_orbs
   global orb_timers
   global spawned

   for orb in all_orbs:
      orb.is_active = False
   spawned = True
   for timer in orb_timers:
      orb_timers.replenish_timer(timer)




def move_orbs():
   global orb_timers
   global all_orbs

   angle = 360
   x_vel, y_vel = 2, 2
   for i in range(0, 4):
      orb = all_orbs[i]
      move_orb(orb, angle, x_vel, y_vel)
      angle -= 90

   if orb_timers.is_empty('wave_1'):
      angle = 350
      for i in range(4, 8):
         orb = all_orbs[i]
         move_orb(orb, angle, x_vel, y_vel)
         angle -= 90
   else:
      orb_timers.countdown('wave_1')

   if orb_timers.is_empty('wave_2'):
      angle = 360
      for i in range(8, 12):
         orb = all_orbs[i]
         move_orb(orb, angle, x_vel, y_vel)
         angle -= 90
   else:
      orb_timers.countdown('wave_2')

def move_orb(orb, angle, x_vel, y_vel):
   speed = get_trajectory(angle, x_vel, y_vel)
   orb.move(speed[0], speed[1])


def get_trajectory(angle, x, y):
   if angle == 0 or angle == 360:
      y = 0
   elif angle == 90:
      x = 0
   elif angle == 180:
      x, y = -x, 0

   elif angle == 270:
      y, x = -y, 0

   elif angle <= 90:
      pass

   elif angle > 90 and angle <= 180:
      x = -x

   elif angle > 180 and angle <= 270:
      x, y = -x, -y

   elif angle > 270 and angle <= 360:
      y = -y

   return (x, y)