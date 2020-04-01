#!/usr/bin/env python
import timer
import pygame
import sprite
from bit_text import Bit_text
import megaman_object
import universal_var
from camera import World_camera

class Debug(object):
   all_timers = timer.Timer()
   all_timers.add_ID('speed_rate', 10)
   hud_background = pygame.Surface((470, 130))

   def debug_init():
      Debug.cursor = megaman_object.Megaman_object('cursor', -50, -100, None, None, True, 15, 15)
      Debug.cursor_speed = 9
      Debug.point_dist_active = False
      Debug.point_dist = [0, 0]

   @classmethod
   def debug_mode(cls, screen):
      World_camera.target_focus = cls.cursor
      pygame.draw.rect(screen, (255,255,255), (300 - cls.cursor.width//2, 300 - cls.cursor.height//2, cls.cursor.width, cls.cursor.height), 2)
      pygame.draw.rect(screen, (255,255,255), (300, 300, cls.cursor.width//2, cls.cursor.height//2))
      cls.hud_background.set_alpha(220)
      cls.hud_background.fill((255,255,255))
      x = 0
      y = 470
      screen.blit(cls.hud_background, (x, y))
      Bit_text.display_text(screen, (x + 10, y + 20), 'co-ordinates: {},{}'.format(World_camera.world_location[0] + 300, 
                                                                                    World_camera.world_location[1] + 300), 2, 2, (0,0,0))
      Bit_text.display_text(screen, (x + 10, y + 50), 'cursor speed: {}'.format(cls.cursor_speed), 2, 2, (0,0,0))
      Bit_text.display_text(screen, (x + 10, y +80), 'point distance: {}, {}'.format(cls.point_dist[0], 
                                                                                 cls.point_dist[1]), 2, 2, (0,0,0))
      keys = pygame.key.get_pressed()

      #To move the cursor
      if keys[pygame.K_UP]:
         cls.cursor.move(0, -cls.cursor_speed)
         if cls.point_dist_active:
            cls.point_dist[1] += -cls.cursor_speed

      if keys[pygame.K_DOWN]:
         cls.cursor.move(0, cls.cursor_speed)
         if cls.point_dist_active:
            cls.point_dist[1] += cls.cursor_speed

      if keys[pygame.K_RIGHT]:
         cls.cursor.move(cls.cursor_speed, 0)
         if cls.point_dist_active:
            cls.point_dist[0] += cls.cursor_speed

      if keys[pygame.K_LEFT]:
         cls.cursor.move(-cls.cursor_speed, 0)
         if cls.point_dist_active:
            cls.point_dist[0] += -cls.cursor_speed

      #to check for change of speed
      for i in range(48, 58): #48-57==key 0-9
         if keys[i]:
            cls.cursor_speed = i - 48

      #to activate point distance calculator
      if keys[pygame.K_x]:
         if cls.point_dist_active == False:
            cls.point_dist = [0, 0]
         cls.point_dist_active = True
      else:
         cls.point_dist_active = False