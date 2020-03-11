import universal_var
import sprite
from projectile import Projectile
import pygame
import misc_function
import display_layer

screen = pygame.display.set_mode((600,600))
display_layer.init()
clock = pygame.time.Clock()
game = True
imgs = misc_function.load_images('projectiles')
p_sprite = sprite.Sprite('main_sprite', 0, 0, 30, 30, [('p', [imgs['boulder_1']], 1)])
p = Projectile('first', 300, 300, sprites=[p_sprite], coll_boxes=None, is_active=False, width=30, height=30, display_layer=3)
p.set(300, 300, 40, 80, 10)
while game:
   screen.fill((0,0,0))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game = False

   for s in sprite.Sprite_surface.all_sprite_surfaces:
      s.update()
      display_layer.push_onto_layer(s, s.display_layer)

   display_layer.display_all_sprite_surf(screen)

   pygame.display.update()
   clock.tick(75)