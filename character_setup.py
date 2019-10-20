import pygame
from misc_function import *
from sprite import *
from megaman import *

megaman_images = load_images('megaman_sprites')

m7 = load_images('m7')

megaman_x = 250
megaman_y = 300

ryu_x = 700
ryu_y = 240

#----------------------------------------------------------------
megaman_right = [megaman_images['walk_2'], megaman_images['walk_1'], megaman_images['walk_2'], megaman_images['walk_3']]
megaman_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_right]

megaman_idle_right = [megaman_images['idle'], megaman_images['idle'], megaman_images['idle'], megaman_images['idle'], megaman_images['idle'], megaman_images['idle_2']]
megaman_idle_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_idle_right]
megaman_idle_shoot_right = [megaman_images['idle_shoot']]
megaman_idle_shoot_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_idle_shoot_right]

megaman_step_right = [megaman_images['step']]
megaman_step_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_step_right]

megaman_shoot_right = [megaman_images['walk_shoot_2'], megaman_images['walk_shoot_1'], megaman_images['walk_shoot_2'], megaman_images['walk_shoot_3']]
megaman_shoot_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_shoot_right]

megaman_jump_right = [megaman_images['jump']]
megaman_jump_left = [pygame.transform.flip(sprite, True, False) for sprite in megaman_jump_right]


megaman_sprite = Sprite(megaman_x, megaman_y, 90, 80, [('right', megaman_right),
                                                                 ('left', megaman_left),
                                                                 ('idle_right', megaman_idle_right),
                                                                 ('idle_left', megaman_idle_left),
                                                                 ('step_right', megaman_step_right),
                                                                 ('step_left', megaman_step_left),
                                                                 ('walk_shoot_right', megaman_shoot_right),
                                                                 ('walk_shoot_left', megaman_shoot_left),
                                                                 ('idle_shoot_right', megaman_idle_shoot_right),
                                                                 ('idle_shoot_left', megaman_idle_shoot_left),
                                                                 ('jump_right', megaman_jump_right),
                                                                 ('jump_left', megaman_jump_left)])

megaman_hit_box = Collision_box('hit_box', megaman_x, megaman_y, 55, 59, (240, 240, 0), x_offset=17)
megaman_feet = Collision_box('feet', megaman_x, megaman_y, 41, 3, (240, 21, 0), x_offset=26, y_offset=61)
megaman_head = Collision_box('head', megaman_x, megaman_y, 43, 2, (200, 21, 0), x_offset=24, y_offset=-3)

player_1 = Main_character('megaman', megaman_x, megaman_y, megaman_sprite, [megaman_hit_box, megaman_feet, megaman_head], 37, 150,
                     controls=[pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_z, pygame.K_x], x_vel=3, jump_speed=13, gravity=True, direction=True,
                     camera=Camera(megaman_x, megaman_y))
#---------------------------------------------------------------------------------------------------------------------------

ryu_right = [m7['3'], m7['4'], m7['5'], m7['6'], m7['7']]
ryu_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_right]
ryu_idle_right = [m7['0'], m7['1'], m7['2']]
ryu_idle_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_idle_right]
ryu_step_right = [m7['2']]
ryu_step_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_step_right]
ryu_jump_right = [m7['4']]
ryu_jump_left = [pygame.transform.flip(sprite, True, False) for sprite in ryu_jump_right]

ryu_sprite = Sprite(ryu_x, ryu_y, 80, 140, [('right', ryu_right),
                                                           ('left', ryu_left),
                                                           ('idle_right', ryu_idle_right),
                                                           ('idle_left', ryu_idle_left),
                                                           ('step_right', ryu_step_right),
                                                           ('step_left', ryu_step_left),
                                                           ('jump_right', ryu_jump_right),
                                                           ('jump_left', ryu_jump_left)])

ryu_box_1 = Collision_box('hit_box', ryu_x, ryu_y, 80, 120, (255, 0, 0), x_offset=0)
ryu_feet = Collision_box('feet', ryu_x, ryu_y, 54, 2, (160, 21, 0), x_offset=13, y_offset=138)
ryu_head = Collision_box('head', ryu_x, ryu_y, 54, 2, (160, 21, 0), x_offset=13, y_offset=-3)
player_2 = Main_character('ryu', ryu_x, ryu_y, ryu_sprite, [ryu_box_1, ryu_feet, ryu_head], 60, 60, x_vel=1, jump_speed=7, gravity=True, direction=True)