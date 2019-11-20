#!/usr/bin/env python
import mega_stack

class Display_layer(object):
   all_layers = []
   display_stack = mega_stack.Stack()
   def __init__(self, n_of_layers):
      for i in range(0, n_of_layers):
         Display_layer.all_layers.append(mega_stack.Stack())

   @classmethod
   def push_onto_layer(cls, sprite_surf):
      cls.all_layers[sprite_surf.display_layer - 1].push(sprite_surf)

   @classmethod
   def update_display_stack(cls):
      for lst in cls.all_layers:
         cls.display_stack.push_update(lst)
         lst.clear()

   @classmethod
   def display_all_surf(cls, surf, screen_width, screen_height):
      cls.update_display_stack()
      for sprite_surf in cls.display_stack:
         try:
            if sprite_surf.is_on_screen(screen_width, screen_height) == True and sprite_surf.is_active == True:
               sprite_surf.display(surf)
         except AttributeError:
            #sprite_surf.display_collboxes(surf)
            pass
         #sprite_surf.display_collboxes(surf)
