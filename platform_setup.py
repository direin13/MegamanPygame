from sprite import *
import universal_names
from misc_function import *
from megaman_object import *

cutman_tiles = load_images('cutman_stage/tile_sprites')

platform_sprite = Sprite(200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']])])
ground = Platform('platform', 310, 400, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

platform_sprite = Sprite(200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']])])
ground = Platform('platform', -80, 400, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

platform_sprite = Sprite(200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']])])
ground = Platform('platform', 80, 400, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

platform_sprite = Sprite(200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']])])
ground = Platform('platform', 600, 400, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

platform_sprite = Sprite(200, 200, 160, 40, [('platform', [cutman_tiles['platform_1_x4']])])
ground = Platform('platform', 900, 400, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

#----------------------------

platform_sprite = Sprite(200, 200, 40, 40, [('platform', [cutman_tiles['platform_1']])])
ground = Platform('platform', 400, 320, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

platform_sprite = Sprite(200, 200, 40, 40, [('platform', [cutman_tiles['platform_1']])])
ground = Platform('platform', 270, 200, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

platform_sprite = Sprite(200, 200, 40, 40, [('platform', [cutman_tiles['platform_1']])])
ground = Platform('platform', 400, 100, platform_sprite, coll_boxes=[Collision_box(universal_names.hitbox, 0, 480, platform_sprite.width, platform_sprite.height)])

platform_sprite = Sprite(200, 200, 40, 30, [('platform', [universal_names.builder['1']])])
ground = Megaman_object('fake_platform', 400, 290, platform_sprite)

