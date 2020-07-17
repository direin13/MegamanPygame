#!/usr/bin/env python
import pygame
import threading

class Song_player(object):
   #This class is used to play songs in a list

   def __init__(self, ID, songs, volume=1.0, current_song=None):
      #--songs must be in a list
      self.ID = ID
      self.songs = songs
      self.volume = volume
      self.current_song = current_song
      self.paused = False
      self.playing = False
      self.running_thread = None
      self.lock_player = False

   def is_playing(self):
      return self.playing


   def set_lock(self, boolean):
      """Locks player to stop other songs from playing over current song"""
      if type(boolean) != bool:
         raise TypeError('Expected a bool, got "{}"'.format(boolean))
      self.lock_player = boolean


   def play_list(self, song_number, start_positon=0.0, loop=False, restart_pos=0.0, lock_player=True):
      if self.lock_player != True or song_number != self.current_song:
         self.stop()
         if lock_player:
            self.set_lock(True)
         self.playing = True

         pygame.mixer.music.set_volume(self.volume)
         pygame.mixer.music.stop()
         self.current_song = song_number
         pygame.mixer.music.load(self.songs[self.current_song])
         pygame.mixer.music.play()
         pygame.mixer.music.set_pos(start_positon)

         self.running_thread = threading.Thread(target=Song_player.play_thread, args=(self, loop, restart_pos))
         self.running_thread.start()


   def play_thread(self, loop=False, restart_pos=0.0):
      while self.playing:
         song_finished = pygame.mixer.music.get_busy() == False
         if self.paused == False:
            if song_finished and loop:
               pygame.mixer.music.rewind()
               pygame.mixer.music.play()
               pygame.mixer.music.set_pos(restart_pos)

            elif song_finished and loop != True:
               self.playing = False

      if pygame.mixer.music.get_busy():
         self.playing = False

      return True


   def toggle(self):
      #--pauses and unpauses the current song--
      if self.paused == False:
         self.paused = True
         pygame.mixer.music.pause()
      elif self.paused == True:
         pygame.mixer.music.unpause()
         self.paused = False


   def set_volume(self, volume):
      #--set volume--
      self.volume = volume


   def stop(self):
      #--stops the song--
      self.playing = False
      if self.running_thread != None and self.running_thread.is_alive():
         self.running_thread.join()
         self.running_thread = None
         pygame.mixer.music.stop()
      self.set_lock(False)

   def __add__(self, other):
      new_songs = self.songs + other.songs
      return Song_player(new_songs)
