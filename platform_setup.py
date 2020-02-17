from sprite import *
import universal_names
from misc_function import *
from megaman_object import *

cutman_tiles = load_images('cutman_stage/tile_sprites')

"""platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']], 1)])
ground = Megaman_object('platform', 310, 400, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=160, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)


platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']], 1)])
ground = Megaman_object('platform', -80, 400, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=160, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)



platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']], 1)])
ground = Megaman_object('platform', 80, 400, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=160, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)


platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']], 1)])
ground = Megaman_object('platform', 600, 400, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=160, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)


platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']], 1)])
ground = Megaman_object('platform', 760, 400, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=160, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)

#----------------------------

platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 40, 40, [('platform', [cutman_tiles['platform_1']], 1)])
ground = Megaman_object('platform', 400, 320, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=40, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)

platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 40, 40, [('platform', [cutman_tiles['platform_1']], 1)])
ground = Megaman_object('platform', 270, 200, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=40, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)



platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 40, 40, [('platform', [cutman_tiles['platform_1']], 1)])
ground = Megaman_object('platform', 100, 100, [platform_sprite], coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)],
                  width=40, height=40)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)

ground = Megaman_object('platform', 1000, 300, sprites=None, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, 200, 40)],
                  width=100, height=100)
Megaman_object.add_to_class_lst(ground, Megaman_object.platforms, ground.ID)"""


"""s = Sprite(universal_names.main_sprite, 0, 0, 600, 600, [('map', [universal_names.megaman_images['map_1'], universal_names.megaman_images['map_2']], 15)])
Megaman_object('map', 0, 0, [s], None, width=600, height=600, display_layer=0)

s = Sprite(universal_names.main_sprite, 0, 0, 600, 600, [('map', [universal_names.megaman_images['map_1'], universal_names.megaman_images['map_2']], 15)])
Megaman_object('map', 603, 0, [s], None, width=600, height=600, display_layer=0)

s = Sprite(universal_names.main_sprite, 0, 0, 600, 600, [('map', [universal_names.megaman_images['map_1'], universal_names.megaman_images['map_2']], 15)])
Megaman_object('map', 1206, 0, [s], None, width=600, height=600, display_layer=0)"""

