#!/usr/bin/env python

import megaman_object
import sprite
import universal_var
import camera
import misc_function

class Gate(megaman_object.Megaman_object):

   def __init__(self, x, y, direction="right"):
      width = 86
      height = 175
      gate_open = [universal_var.prop_images['gate_1'], universal_var.prop_images['gate_2'], universal_var.prop_images['gate_3'],
                         universal_var.prop_images['gate_4'], universal_var.misc_images['blank']]

      gate_close = gate_open[::-1]

      gate_sprite = sprite.Sprite(universal_var.main_sprite, x, y, width, height,
                                 [('gate_open', gate_open, 22),
                                  ('gate_close', gate_close, 22),
                                  ('gate_idle', [universal_var.prop_images['gate_1']], 22)])

      super().__init__("gate", x, y, [gate_sprite], None, True, width, height)
      self.x = x
      self.y = y
      self.transition_collbox = camera.Transition_box('gate_tbox', x + 30, y, direction=direction)
      self.play_gate_sound = True


   def display(self, surf):
      self.update_sprite(universal_var.main_sprite, auto_reset=False)
      if camera.Transition_box.current_box == self.transition_collbox and camera.camera_transitioning():
         if camera.transition_start():
            self.display_animation(universal_var.main_sprite, surf, "gate_open")
            if self.play_gate_sound:
               misc_function.play_sound('gate', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume)
               self.play_gate_sound = False

         elif camera.transition_end():
            self.display_animation(universal_var.main_sprite, surf, "gate_close")
            if self.play_gate_sound:
               misc_function.play_sound('gate', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume) 
               self.play_gate_sound = False

         else:
            self.play_gate_sound = True
      else:
         self.display_animation(universal_var.main_sprite, surf, "gate_idle")
         self.play_gate_sound = True
         


   def update(self):
      sprite.Sprite_surface.update(self)