from sprite import Sprite_surface, Collision_box
import universal_var
from megaman_object import Megaman_object
from timer import Timer
from megaman import Megaman
import camera


class Boss_room(Megaman_object):
   battle_has_end = False
   def __init__(self, boss, x, y, width, height):
      c = [Collision_box(universal_var.hitbox, x, y, width, height, (130, 190, 140))]
      super().__init__('Boss_room', x, y, sprites=None, coll_boxes=c,
                        width=width, height=height, display_layer=5)

      self.battle_has_init = False
      self.battle_has_end = False
      self.all_timers = Timer()
      self.all_timers.add_ID('time_till_start', 40)
      self.all_timers.add_ID('time_till_boss_spawn', 60)
      self.all_timers.add_ID('time_till_refill_bar', 130)
      self.all_timers.add_ID('time_till_end', 550)
      self.all_timers.add_ID('time_till_end_song', 160)
      self.boss = boss


   def check_player_collision(self):
      if len(Megaman.all_sprite_surfaces) != 0:
         trigger_box_collision = self.check_collision_lst(Megaman.all_sprite_surfaces, universal_var.hitbox, universal_var.hitbox)
         if trigger_box_collision.is_empty() != True:
            return True
      return False


   def spawn_boss(self):
      if self.all_timers.is_finished('time_till_start') != True:
         self.all_timers.countdown('time_till_start')
         self.music_lock = False

      else:
         self.boss.health_bar.is_active = True
         universal_var.songs.play_list(song_number=5)
         if self.all_timers.is_finished('time_till_boss_spawn') != True:
            self.all_timers.countdown('time_till_boss_spawn')
         elif self.battle_has_init != True and self.boss.is_active != True:
            self.boss.spawn()

         if self.boss.is_active:
            if self.all_timers.is_finished('time_till_refill_bar') != True:
               self.all_timers.countdown('time_till_refill_bar')
            elif self.boss.health_bar.is_full() != True:
               self.boss.health_bar.refill(11)


   def end_level(self):
      if self.all_timers.is_finished('time_till_end') != True:
         self.all_timers.countdown('time_till_end')
      else:
         Boss_room.battle_has_end = True

      if self.all_timers.is_finished('time_till_end_song') != True:
         self.all_timers.countdown('time_till_end_song')
      if self.all_timers.get_ID('time_till_end_song')['curr_state'] == 1:
         universal_var.songs.play_list(song_number=6)


   def update(self):
      if len(Megaman.all_sprite_surfaces) != 0:
         m = Megaman.all_sprite_surfaces[0]
         if self.check_player_collision():
            if self.battle_has_init != True and camera.camera_transitioning() != True:
               m.disable_keys()
               self.spawn_boss()
            elif self.battle_has_init and self.battle_has_end != True:
               m.enable_keys()

            if self.battle_has_end:
               m.disable_keys()
               self.end_level()

            if (self.battle_has_init and self.battle_has_end != True) and self.boss.is_alive() != True and self.boss.is_active != True:
               self.battle_has_end = True
               universal_var.songs.stop()

         if universal_var.game_reset:
            self.battle_has_init = False
            self.battle_has_end = False
            self.boss.health_bar.points = 0
            m.enable_keys()
            for ID in self.all_timers:
               self.all_timers.replenish_timer(ID)
      Sprite_surface.update(self)