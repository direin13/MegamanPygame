#!/usr/bin/env python
import pygame
import sprite
import megaman_object
import universal_var
import enemy
import camera
import gate
from megaman import Megaman
import items
import concrete_man
from concrete_shot import Concrete_shot
import projectile
from megaman_death_orb import Death_orb
from p_shooter import P_shooter
import intro_sequence
from title_screen import Title_screen
from timer import Timer

level_dict = {'concrete_man': [concrete_man.props, concrete_man.coll_boxes, concrete_man.enemies, concrete_man.all_items]}
game_timers = Timer()
game_timers.add_ID('time_till_game_start', 550) #550
game_timers.add_ID('init_star_background', 90)
Title_screen.init()

def clear_all_lists():
   sprite.Sprite_surface.all_sprite_surfaces.clear()
   sprite.Sprite_surface.all_name_count.clear()
   megaman_object.Megaman_object.all_sprite_surfaces.clear()
   megaman_object.Megaman_object.platforms.clear()
   megaman_object.Megaman_object.hazards.clear()
   enemy.Enemy.all_sprite_surfaces.clear()
   camera.Camera_box.all_camera_box.clear()
   camera.Transition_box.all_transition_box.clear()
   Megaman.all_sprite_surfaces.clear()
   items.Item.drop_list.clear()
   enemy.Hoohoo_boulder.mini_boulder_1_stack.clear()
   enemy.Hoohoo_boulder.mini_boulder_2_stack.clear()
   projectile.Enemy_projectile_1.all_p_stack.clear()
   projectile.Enemy_projectile_1.all_p_lst.clear()
   Concrete_shot.all_p_stack.clear()
   Concrete_shot.all_p_lst.clear()
   Death_orb.all_orbs_lst.clear()
   Death_orb.all_orbs_stack.clear()
   P_shooter.all_p_stack.clear()
   P_shooter.all_p_lst.clear()


def load_megaman_objects(props=None, coll_boxes=None, enemies=None, all_items=None, spawn_megaman=False, m_x=0, m_y=0):
   # making all the game objects at once
   if spawn_megaman:
      megaman = Megaman('megaman', m_x, m_y, controls=[pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_z, pygame.K_x])

   n = 0
   if props != None:
      for lst in props:
         prop_name = lst[0]

         if prop_name == 'bg':
            x, y, width, height, display_layer, rgb = lst[1][0], lst[1][1], lst[2][0], lst[2][1], lst[4], lst[5]
            frames = [universal_var.background_images[i] for i in lst[3][0]]  
            s = sprite.Sprite(universal_var.main_sprite, x, y, width, height, 
               active_frames=[('bg_{}'.format(n), frames, lst[3][1])], change_rgb_value=True, rgb=rgb)
            obj = megaman_object.Megaman_object('bg_{}'.format(n), x, y, sprites=[s], coll_boxes=None, width=width, height=height, display_layer=display_layer)
            n += 1

         elif prop_name == 'gate':
            x, y = lst[1][0], lst[1][1]
            gate.Gate(x, y)


   if all_items != None:
      for lst in all_items:
         objType, x, y = lst[0], lst[1], lst[2]
         if objType == 'e_life':
            items.Extra_life(x, y, is_drop=False)

         elif objType == 's_hcap':
            items.Health_capsule(x, y, False, is_drop=False)  

         elif objType == 'l_hcap':
            items.Health_capsule(x, y, True, is_drop=False)


   if coll_boxes != None:
      for lst in coll_boxes:
         x, y, objType = lst[0][0], lst[0][1], lst[2]
         if objType == 'platform':
            width, height = lst[1][0], lst[1][1]
            c = [sprite.Collision_box(universal_var.hitbox, x, y, width, height)]
            ground = megaman_object.Megaman_object('platform', x, y, sprites=None, coll_boxes=c,
                           width=width, height=height, display_layer=5)
            megaman_object.Megaman_object.add_to_class_lst(ground, megaman_object.Megaman_object.platforms, ground.ID)

         elif objType == 'c_box':
            width, height = lst[1][0], lst[1][1]
            camera_box = camera.Camera_box('c_box', x, y, width, height)

         elif objType == 't_box':
            size, direction = lst[1], lst[3]
            transition_box = camera.Transition_box('t_box', x, y, size=size, direction=direction)


   if enemies != None:
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

         if enemy_name == 'concrete_man':
            x, y, spawn = lst[0][0], lst[0][1], lst[4]
            collbox_x, collbox_y, collbox_width, collbox_height = lst[2][0], lst[2][1], lst[3][0], lst[3][1]

            c = [sprite.Collision_box(universal_var.hitbox, collbox_x, collbox_y, collbox_width, collbox_height, (130, 190, 140))]
            trigg_collbox = megaman_object.Megaman_object('platform', collbox_x, collbox_y, sprites=None, coll_boxes=c,
                                                   width=collbox_width, height=collbox_height, display_layer=5)

            concrete_man.Concrete_man(x, y, trigg_collbox, spawn)

   items.Item.drop_list_init()


def boss_intro_sequence(boss_name):
   global game_timers
   if game_timers.is_full('time_till_game_start'):
      clear_all_lists()
      stage_name = ' '.join(boss_name.split('_'))
      intro_sequence.Stage_rectangle(300, stage_name)
      universal_var.songs.play_list(song_number=3)

   if game_timers.is_finished('init_star_background') != True:
      game_timers.countdown('init_star_background')
   elif intro_sequence.Star.init != True:
      intro_sequence.Star.init_star_background()
      load_megaman_objects(enemies=[[(240, -400), boss_name, (0,0), (0,0), True]])
   game_timers.countdown('time_till_game_start')