import pygame
from megaman import *

megaman_x = 250
#megaman_y = 350
megaman_y = 410
megaman_width = 90
megaman_height = 80
m_idle_speed = 150
m_run_speed = 37

ryu_x = -100
ryu_y = 240
ryu_speed = 70


#-------------------------------------------------------------

#--megaman

player_1 = Megaman('megaman', megaman_x, megaman_y, controls=[pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_z, pygame.K_x])

#---------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------
"""
ryu = [universal_names.m7['3'], universal_names.m7['4'], universal_names.m7['5'], universal_names.m7['6'], universal_names.m7['7']]

ryu_idle = [universal_names.m7['0'], universal_names.m7['1'], universal_names.m7['2']]

ryu_step = [universal_names.m7['2']]
ryu_jump = [universal_names.m7['4']]

ryu_sprite = Sprite(universal_names.main_sprite, ryu_x, ryu_y, 80, 140,  [('walk', ryu, ryu_speed),
                                             ('idle', ryu_idle, ryu_speed),
                                             ('step', ryu_step, ryu_speed),
                                             ('jump', ryu_jump, ryu_speed)])

ryu_box_1 = Collision_box(universal_names.hitbox, ryu_x, ryu_y, 80, 120, (255, 0, 0), x_offset=0)
ryu_feet = Collision_box(universal_names.feet, ryu_x, ryu_y, 54, 2, (160, 21, 0), x_offset=13, y_offset=138)
ryu_head = Collision_box(universal_names.head, ryu_x, ryu_y, 54, 2, (160, 21, 0), x_offset=13, y_offset=-3)
player_2 = Megaman('ryu', ryu_x, ryu_y, [ryu_sprite], [ryu_box_1, ryu_feet, ryu_head], gravity=False, x_vel=1, jump_speed=7, direction=True, 
                   width=80, height=140)"""