from sprite import *
from universal_names import *
from megaman import *

camera_box_1 = Camera_box('static', -100, 100, coll_boxes=[Collision_box(hitbox, 300, 400, 200, 400)])

camera_box_2 = Camera_box('static', 500, -50, coll_boxes=[Collision_box(hitbox, 300, 400, 200, 1000)])

camera_box_2 = Camera_box('special_static', 700, -50, coll_boxes=[Collision_box(hitbox, 300, 400, 200, 1000)])