from camera import *
import universal_names
from megaman import *

camera_box_1 = Camera_box('static', -95, -50, 280, 1000)

camera_box_1 = Camera_box('static', -390, -50, 280, 1000)

camera_box_2 = Camera_box('static', 482, -50, 280, 1000)

camera_box_3 = Camera_box('static', 782, -50, 280, 1000)

transition_box = Transition_box('transition_box', 755, 0, size=1000, direction='right')

transition_box = Transition_box('transition_box', -85, 0, size=1000, direction='left')

transition_box = Transition_box('transition_box', 150, 595, direction='down')

transition_box = Transition_box('transition_box', 150, 1195, direction='down')

transition_box = Transition_box('transition_box', 0, -5, size=1000, direction='up')
