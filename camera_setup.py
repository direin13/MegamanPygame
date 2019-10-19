from sprite import *
from megaman import *

camera_box_1 = Camera_box('static', -100, 100, coll_boxes=[Collision_box('hit_box', 300, 400, 200, 400)])

camera_box_2 = Camera_box('static', 700, 100, coll_boxes=[Collision_box('hit_box', 300, 400, 200, 400)])