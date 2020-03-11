#!/usr/bin/env python
import pygame
import sprite
import megaman_object
import universal_var
import enemy
import camera
import gate
from megaman import Megaman

props = [
              ['background', (0,0), (2400, 600), (['map_1'], 30)], ['background', (2399,0), (1800, 600), (['map_2'], 30)], 
              ['background', (3600,600), (600, 600), (['map_3'], 30)], ['background', (2400,1200), (1800, 600), (['map_4'], 30)], 
              ['background', (2400,1800), (600, 1800), (['map_5'], 30)], ['background', (2400,3600), (3000, 600), (['map_6'], 30)],
              ['gate', (4157,3846)], ['gate', (4757,3846)]
        ]

coll_boxes = [
              [(-20,0), (20,600), 'p'], [(0,472), (1806,40), 'p'], [(690,429), (345, 40), 'p'], [(1208,429), (345, 40), 'p'], 
              [(1728,385), (345, 40), 'p'], [(2074,342), (342,642), 'p'], [(2419,472), (254,206), 'p'], [(2764,472), (257,317), 'p'],
              [(3110,429), (170,402), 'p'], [(3414,472), (559,173), 'p'], [(3719,387), (230,103), 'p'], [(3803,302), (167,203), 'p'],
              [(3759,129), (213,171), 'p'], [(3455,249), (173,46), 'p'], [(3455,0), (85,249), 'p'], [(4112,-182), (87,2000), 'p'],
              [(3769,867), (351,127), 'p'], [(3630,1117), (257,125), 'p'], [(2907,1628), (2067,1876), 'p'], [(3565,642), (59,771), 'p'],
              [(3590,1300), (15,771), 'p'], [(2986,1300), (15,771), 'p'], [(2403,1200), (82,3198), 'p'], [(2568,1997), (258,44), 'p'],
              [(2818,2231), (85,41), 'p'], [(2492,2231), (85,41), 'p'], [(2656,2043), (42,1743), 'p'], [(2698,2584), (129,41), 'p'],
              [(2775,2704), (129,41), 'p'], [(2700,2827), (129,41), 'p'], [(2682,2400), (254,6), 'p'], [(2483,3223), (90,41), 'p'],
              [(2569,3400), (90,41), 'p'], [(2659,3776), (427,43), 'p'], [(2827,4066), (1422,144), 'p'], [(2483,4025), (348,172), 'p'],
              [(3790,4022), (1058,178), 'p'], [(4030,3515), (815,330), 'p'], [(2994,3515), (10,1000), 'p'],
              [(4848,4157), (550,42), 'p'], [(4224,3842), (16,213), 'p'], [(4821,3847), (24,193), 'p'], [(5359,3760), (44,435), 'p'],
              [(3269,3776), (79,43), 'p'], [(3556,3776), (38,43), 'p']
             ]

camera_boxes = [
                [(0,-300), (267,1500)], [(3918,-178), (283,1278)], [(3600, 600), (600, 1200)], [(3000, 1200), (600, 600)], 
                [(2400,1200), (600, 3000)], [(3000,3527), (265,1278)], [(3923,3527), (1500,1278)]
               ]

transition_boxes = [
                    [(3853, 578), 400,'down'], [(3600, 1184), 800,'down'], [(3607, 1423), 446,'left'], [(3000, 1423), 546,'left'],
                    [(2410, 1765), 581,'down'], [(2410, 2391), 581,'down'], [(2407, 2978), 605,'down'], [(2407, 3558), 605,'down'],
                    [(2990, 3623), 546,'right']
                   ]

enemies = [
           [(3735,370), 'met', False, 130, 50], [(4196,823), 'lasor', 45, -6], [(3592-1400,1072), 'lasor', 148, 6], 
           [(2392-1400,1950), 'lasor', 73, 6], [(3074,2187), 'lasor', 53, -6], [(2393-1400,2539), 'lasor', 3, 6], 
           [(3074,2661), 'lasor', 50, -6], [(2393-1400,2783), 'lasor', 78, 6], [(2717,620), 'det', 35, 73, 150, 600],
           [(2717,620), 'det', 180, 57, 140, 600], [(3059,620), 'det', 25, 70, 150, 600], [(3059,620), 'det', 180, 70, 150, 600],
           [(3347,620), 'det', 25, 67, 170, 600], [(3347,620), 'det', 180, 77, 170, 600],
           [(3289,3755), 'met', False, 160, 50], [220, 'hoohoo', 50, (603,198), (750,279)], [220, 'hoohoo', 170, (603,198), (750,279)],
           [230, 'hoohoo', 40, (1360,128), (1245,479)], [90, 'hoohoo', 100, (1360,128), (1045,479)], [80, 'hoohoo', 70, (2626,171), (567,479)], 
           [280, 'hoohoo', 60, (2484,3679), (500,600)], [90, 'hoohoo', 70, (3202,3582), (576,479)],
           [(3130,1549), 'paozo', True], [(3681, 4064), 'big_stomper', 22], [(3321, 4064), 'big_stomper', 22]
          ]


# making all the different objects at once
n = 0
for lst in props:
   prop_name = lst[0]
   if prop_name == 'background':
      x, y, width, height = lst[1][0], lst[1][1], lst[2][0], lst[2][1]
      frames = [universal_var.background_images[i] for i in lst[3][0]]
      s = sprite.Sprite(universal_var.main_sprite, x, y, width, height, 
         active_frames=[('map_{}'.format(n), frames, lst[3][1])])
      obj = megaman_object.Megaman_object('map_{}'.format(n), x, y, sprites=[s], coll_boxes=None, width=width, height=height, display_layer=0)
      n += 1

   if prop_name == 'gate':
      x, y = lst[1][0], lst[1][1]
      gate.Gate(x, y)


for lst in coll_boxes:
   x, y, width, height = lst[0][0], lst[0][1], lst[1][0], lst[1][1]
   objType = lst[2]
   c = [sprite.Collision_box(universal_var.hitbox, x, y, width, height)]
   ground = megaman_object.Megaman_object('platform', x, y, sprites=None, coll_boxes=c,
                  width=width, height=height, display_layer=5)
   if objType == 'p':
      megaman_object.Megaman_object.add_to_class_lst(ground, megaman_object.Megaman_object.platforms, ground.ID)


for lst in enemies:
   enemy_name = lst[1]

   if enemy_name == 'met':
      x, y = lst[0][0], lst[0][1]
      direction, trigger_width, trigger_height = lst[2], lst[3], lst[4]
      enemy.Met('met', x, y, direction, trigger_width, trigger_height)

   if enemy_name == 'det':
      x, y = lst[0][0], lst[0][1]
      start_time, time_to_apex, trigger_width, trigger_height = lst[2], lst[3], lst[4], lst[5]
      enemy.Detarnayappa('Detarnayappa', x, y, start_time, time_to_apex, trigger_width, trigger_height)

   if enemy_name == 'lasor':
      x, y = lst[0][0], lst[0][1]
      start_offset, x_vel = lst[2], lst[3]
      enemy.Lasor('lasor', x, y, start_offset, x_vel)

   if enemy_name == 'hoohoo':
      hoohoo_y, start_time = lst[0], lst[2]
      collbox_x, collbox_y, collbox_width, collbox_height = lst[3][0], lst[3][1], lst[4][0], lst[4][1]

      c = [sprite.Collision_box(universal_var.hitbox, collbox_x, collbox_y, collbox_width, collbox_height, (130, 190, 40))]
      trigg_collbox = megaman_object.Megaman_object('platform', collbox_x, collbox_y, sprites=None, coll_boxes=c,
                                             width=collbox_width, height=collbox_height, display_layer=5)

      enemy.Hoohoo('hoohoo', hoohoo_y, start_time, trigg_collbox)

   if enemy_name == 'paozo':
      x, y, direction = lst[0][0], lst[0][1], lst[2]
      enemy.Paozo(x, y, direction)

   if enemy_name == 'big_stomper':
      x, y, damage_points = lst[0][0], lst[0][1], lst[2]
      enemy.Big_stomper(x, y, damage_points)

for lst in camera_boxes:
   x, y, width, height =  lst[0][0], lst[0][1], lst[1][0], lst[1][1]
   camera_box = camera.Camera_box('c_box', x, y, width, height)

for lst in transition_boxes:
   x, y, size, direction = lst[0][0], lst[0][1], lst[1], lst[2]
   transition_box = camera.Transition_box('t_box', x, y, size=size, direction=direction)

megaman_x = 250
megaman_y = 410
megaman_width = 90
megaman_height = 80
m_idle_speed = 150
m_run_speed = 37

player_1 = Megaman('megaman', megaman_x, megaman_y, controls=[pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_z, pygame.K_x])