from sprite import *
import universal_names
from misc_function import *
from megaman_object import *

cutman_tiles = load_images('cutman_stage/tile_sprites')

platform_sprite = Sprite(universal_names.main_sprite, 200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']], 1)])
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

"""s = Sprite(universal_names.main_sprite, 0, 0, 502, 502, [('map', [universal_names.megaman_images['Map_1']], 1)])
Megaman_object('map', -80, -3, [s], None, width=500, height=500)"""