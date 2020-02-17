#!/usr/bin/env python
import mega_stack

#displayer layer will determine where each sprite surface is displayed, layers go from 0-5 (back-front)
all_layers = []
display_stack = mega_stack.Stack()


def init(n_of_layers=6):
   global all_layers

   for i in range(0, n_of_layers):
      all_layers.append(mega_stack.Stack())


def push_onto_layer(sprite_surf, layer):
   global all_layers

   all_layers[layer].push(sprite_surf)


def update_display_stack():
   global all_layers
   global display_stack

   for lst in all_layers:
      display_stack.push_update(lst)
      lst.clear()


def display_all_sprite_surf(surf, screen_width, screen_height, display_collboxes=False, alpha=100):
   global display_stack

   update_display_stack()
   x = 0
   for sprite_surf in display_stack:
      try:
         if sprite_surf.is_active:
            sprite_surf.display(surf)
      except AttributeError:
         #sprite_surf.display_collboxes(surf)
         pass
      if display_collboxes == True:
         if sprite_surf.is_on_screen(screen_width, screen_height):
            sprite_surf.display_collboxes(surf, alpha)
