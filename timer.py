#!/usr/bin/env python
import time

class Timer(object):
   def __init__(self):
      self.timer_states = {}
      self.all_timers = {}

   def add_ID(self, ID, speed):
      #--this will add a new ID into the dictionaries, be wary of ID name choices, as they can be overwritten
      self.all_timers[ID] = speed
      self.timer_states[ID] = speed

   def countdown(self, ID, speed=None, loop=False):
      #--will subtract 1 from the ID in the dictionary and return True if ID reaches 0 to imitate a real timer, can loop timer
      if ID not in self.all_timers:
         self.add_ID(ID, speed)

      if speed == None:
         speed = self.all_timers[ID]
      else:
         self.all_timers[ID] = speed
         if self.timer_states[ID] > speed:
            self.timer_states[ID] = speed

      self.timer_states[ID] -= 1
      if self.timer_states[ID] >= 0:
         return True
      else:
         if loop == False:
            self.timer_states[ID] = 0
            return False
         else:
            self.timer_states[ID] = self.all_timers[ID]
            return False

   def replenish_timer(self, ID, n=None):
      if n == None:
         self.timer_states[ID] = self.all_timers[ID]
      else:
         self.timer_states[ID] = n

   def check_ID(self, ID):
      return self.timer_states[ID]

   def is_empty(self, ID):
      return self.timer_states[ID] == 0

   def print_timer(self, ID):
      print('{}: {}'.format(ID, self.timer_states[ID]))

   def __iter__(self):
      for timer in self.all_timers.keys():
         yield timer
