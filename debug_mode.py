#!/usr/bin/env python
import timer
import pygame
import sprite
import bit_text
import megaman_object
import universal_names

all_timers = timer.Timer()
all_timers.add_ID('speed_rate', 10)
hud_background = pygame.Surface((470, 130))
cursor = megaman_object.Megaman_object('cursor', -50, -100, None, None, True, 15, 15)
cursor_speed = 9
point_dist_active = False
point_dist = [0, 0]

def debug(screen):
   global cursor_speed
   global point_dist
   global point_dist_active

   universal_names.camera.sprite_surf = cursor
   pygame.draw.rect(screen, (255,255,255), (300 - cursor.width//2, 300 - cursor.height//2, cursor.width, cursor.height), 2)
   pygame.draw.rect(screen, (255,255,255), (300, 300, cursor.width//2, cursor.height//2))
   hud_background.set_alpha(220)
   hud_background.fill((255,255,255))
   x = 0
   y = 470
   screen.blit(hud_background, (x, y))
   bit_text.display_text(screen, (x + 10, y + 20), 'co-ordinates: {},{}'.format(universal_names.world_location[0] + 300, 
                                                                                 universal_names.world_location[1] + 300), 2, 2, (0,0,0))
   bit_text.display_text(screen, (x + 10, y + 50), 'cursor speed: {}'.format(cursor_speed), 2, 2, (0,0,0))
   bit_text.display_text(screen, (x + 10, y +80), 'point distance: {}, {}'.format(point_dist[0], 
                                                                              point_dist[1]), 2, 2, (0,0,0))
   keys = pygame.key.get_pressed()

   #To move the cursor
   if keys[pygame.K_UP]:
      cursor.move(0, -cursor_speed)
      if point_dist_active:
         point_dist[1] += -cursor_speed

   if keys[pygame.K_DOWN]:
      cursor.move(0, cursor_speed)
      if point_dist_active:
         point_dist[1] += cursor_speed

   if keys[pygame.K_RIGHT]:
      cursor.move(cursor_speed, 0)
      if point_dist_active:
         point_dist[0] += cursor_speed

   if keys[pygame.K_LEFT]:
      cursor.move(-cursor_speed, 0)
      if point_dist_active:
         point_dist[0] += -cursor_speed

   #to check for change of speed
   for i in range(48, 58):
      if keys[i]:
         cursor_speed = i - 48

   #to activate point distance calculator
   if keys[pygame.K_x]:
      if point_dist_active == False:
         point_dist = [0, 0]
      point_dist_active = True
   else:
      point_dist_active = False