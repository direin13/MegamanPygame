#!/usr/bin/env python
import pygame
class Song_player(object):
   #This class is used to play songs in a list

   def __init__(self, ID, songs, volume=1.0, current_song=0):
      #--songs must be in a list
      self.ID = ID
      self.songs = songs
      self.volume = volume
      self.current_song = current_song
      self.paused = False


   def play_list(self, song_length, fade_time=0, song_number=None):
      #--begins playing the list of songs in self.songs. If song number specified then that song in the list will be played.
      #--song length refers to how long the current song should be played
      #--fade time refers to the songs fadeout in seconds. E.g if fade_time=2 then the fadeout from song_lenght will be 2 seconds.
      pygame.mixer.music.set_volume(self.volume)

      if song_number != None and song_number != self.current_song:
         self.stop()
         self.current_song = song_number
         pygame.mixer.music.load(self.songs[self.current_song])
         pygame.mixer.music.play()
      else:
         pass

      if self.paused == False:
         if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(self.songs[self.current_song])
            pygame.mixer.music.play()
      else:
         pass


   def toggle(self):
      #--pauses and unpauses the current song if using play_list()--
      if self.paused == False:
         self.paused = True
         pygame.mixer.music.pause()
      elif self.paused == True:
         pygame.mixer.music.unpause()
         self.paused = False


   def next_song(self, song_length, fade_time=0):
      #--change the current song to next song in self.songs--
      pygame.mixer.music.stop()
      self.play_list(song_length, fade_time)


   def previous_song(self, song_length):
      #--change the current song to previous song in self.songs--
      pygame.mixer.music.stop()
      self.current_song -= 2
      if self.current_song < 0:
         self.current_song = len(self.songs) - 1
      self.play_list(song_length)


   def add_songs(self, songs):
      #--adds songs in a list to self.songs
      for song in songs:
         self.songs.append(song)


   def remove_songs(self, songs):
      #--remove songs in a list from self.songs--
      for song in songs:
         try:
            self.songs.remove(song)
         except ValueError:
            print('Error: {} is not in the list'.format(song))


   def set_volume(self, volume):
      #--set volume--
      self.volume = volume


   def play_song(self, song, loops=0):
      #--play a specified song--
      pygame.mixer.music.pause()
      i = 0
      try:
         while song != self.songs[i]:
            i += 1
      except IndexError:
         print('Error: {} not in {}'.format(song, self.ID))
         quit()
      pygame.mixer.music.set_volume(self.volume)
      self.current_song = i
      pygame.mixer.music.load(self.songs[self.current_song])
      pygame.mixer.music.play(loops=loops)


   def stop(self):
      #--stops the song--
      pygame.mixer.music.stop()

   def __add__(self, other):
      new_songs = self.songs + other.songs
      return Song_player(new_songs)
