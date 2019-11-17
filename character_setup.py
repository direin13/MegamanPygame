import pygame
import universal_names
from misc_function import *
from sprite import *
from enemy import *
from megaman_object import *
from megaman import *

megaman_x = 250
megaman_y = 300
megaman_width = 90
megaman_height = 80
m_idle_speed = 150
m_run_speed = 37

ryu_x = -100
ryu_y = 240
ryu_speed = 70

camera = Camera(megaman_x, megaman_y)

#----------------------------------------------------------------

#--sprites
megaman_right = [universal_names.megaman_images['walk_2'], universal_names.megaman_images['walk_1'], universal_names.megaman_images['walk_2'], universal_names.megaman_images['walk_3']]
megaman_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_right]

megaman_idle_right = [universal_names.megaman_images['idle'], universal_names.megaman_images['idle'], universal_names.megaman_images['idle'], universal_names.megaman_images['idle'], universal_names.megaman_images['idle'], universal_names.megaman_images['idle_2']]
megaman_idle_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_idle_right]
megaman_idle_shoot_right = [universal_names.megaman_images['idle_shoot']]
megaman_idle_shoot_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_idle_shoot_right]

megaman_step_right = [universal_names.megaman_images['step']]
megaman_step_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_step_right]

megaman_shoot_right = [universal_names.megaman_images['walk_shoot_2'], universal_names.megaman_images['walk_shoot_1'], universal_names.megaman_images['walk_shoot_2'], universal_names.megaman_images['walk_shoot_3']]
megaman_shoot_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_shoot_right]

megaman_jump_right = [universal_names.megaman_images['jump']]
megaman_jump_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_jump_right]
megaman_shoot_jump_right = [universal_names.megaman_images['shoot_jump']]
megaman_shoot_jump_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_shoot_jump_right]

megaman_damage_right = [universal_names.megaman_images['damage']]
megaman_damage_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_damage_right]


megaman_sprite = Sprite(universal_names.main_sprite, megaman_x, megaman_y, megaman_width, megaman_height, [('walk_right', megaman_right, m_run_speed),
                                                       ('walk_left', megaman_left, m_run_speed),
                                                       ('idle_right', megaman_idle_right, m_idle_speed),
                                                       ('idle_left', megaman_idle_left, m_idle_speed),
                                                       ('step_right', megaman_step_right, m_run_speed),
                                                       ('step_left', megaman_step_left, m_run_speed),
                                                       ('shoot_walk_right', megaman_shoot_right, m_run_speed),
                                                       ('shoot_walk_left', megaman_shoot_left, m_run_speed),
                                                       ('shoot_idle_right', megaman_idle_shoot_right, m_run_speed),
                                                       ('shoot_idle_left', megaman_idle_shoot_left, m_run_speed),
                                                       ('jump_right', megaman_jump_right, m_run_speed),
                                                       ('jump_left', megaman_jump_left, m_run_speed),
                                                       ('shoot_jump_right', megaman_shoot_jump_right, m_run_speed),
                                                       ('shoot_jump_left', megaman_shoot_jump_left, m_run_speed),
                                                       ('damage_right', megaman_damage_right, m_idle_speed),
                                                       ('damage_left', megaman_damage_left, m_idle_speed)])

effects = Sprite('effects', megaman_x, megaman_y, 90, 80, [('spark_effect', [universal_names.effect_images['spark']], 1)])
#--collision boxes

megaman_hit_box = Collision_box(universal_names.hitbox, megaman_x, megaman_y, 55, 59, (240, 240, 0), x_offset=17)
megaman_feet = Collision_box(universal_names.feet, megaman_x, megaman_y, 41, 3, (240, 21, 0), x_offset=26, y_offset=61)
megaman_head = Collision_box(universal_names.head, megaman_x, megaman_y, 43, 2, (200, 21, 0), x_offset=24, y_offset=-3)

#--megaman

player_1 = Megaman('megaman', megaman_x, megaman_y, [megaman_sprite, effects], [megaman_hit_box, megaman_feet, megaman_head], gravity=True,
                    controls=[pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_z, pygame.K_x], max_x_vel=3, jump_speed=10, direction=True,
                    camera=camera, width=megaman_width, height=megaman_height, health_points=100)
#---------------------------------------------------------------------------------------------------------------------------

idle_enemy = [universal_names.builder['1']]
explosion_enemy = [universal_names.effect_images['explosion_1'], universal_names.effect_images['explosion_2'], universal_names.effect_images['explosion_3']]
enemy_sprite = Sprite(universal_names.main_sprite, 200, 200, 40, 30, [('idle', idle_enemy, 1),
                                                                      ('explosion', explosion_enemy, 15)])
enemy_hit_box = Collision_box(universal_names.hitbox, 400, 290, 36, 30, (240, 240, 0), x_offset=2)
enemy_test= Enemy('enemy_test', 400, 290, [enemy_sprite], [enemy_hit_box], width=40, height=30, health_points=10, damage_points=10)


#---------------------------------------------------------------------------------------------------------------------------
"""
ryu_right = [universal_names.m7['3'], universal_names.m7['4'], universal_names.m7['5'], universal_names.m7['6'], universal_names.m7['7']]
ryu_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_right]
ryu_idle_right = [universal_names.m7['0'], universal_names.m7['1'], universal_names.m7['2']]
ryu_idle_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_idle_right]
ryu_step_right = [universal_names.m7['2']]
ryu_step_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_step_right]
ryu_jump_right = [universal_names.m7['4']]
ryu_jump_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_jump_right]

ryu_sprite = Sprite(universal_names.main_sprite, ryu_x, ryu_y, 80, 140,  [('walk_right', ryu_right, ryu_speed),
                                             ('walk_left', ryu_left, ryu_speed),
                                             ('idle_right', ryu_idle_right, ryu_speed),
                                             ('idle_left', ryu_idle_left, ryu_speed),
                                             ('step_right', ryu_step_right, ryu_speed),
                                             ('step_left', ryu_step_left, ryu_speed),
                                             ('jump_right', ryu_jump_right, ryu_speed),
                                             ('jump_left', ryu_jump_left, ryu_speed)])

ryu_box_1 = Collision_box(universal_names.hitbox, ryu_x, ryu_y, 80, 120, (255, 0, 0), x_offset=0)
ryu_feet = Collision_box(universal_names.feet, ryu_x, ryu_y, 54, 2, (160, 21, 0), x_offset=13, y_offset=138)
ryu_head = Collision_box(universal_names.head, ryu_x, ryu_y, 54, 2, (160, 21, 0), x_offset=13, y_offset=-3)
player_2 = Megaman('ryu', ryu_x, ryu_y, [ryu_sprite], [ryu_box_1, ryu_feet, ryu_head], gravity=False, x_vel=1, jump_speed=7, direction=True, 
                   width=80, height=140)"""