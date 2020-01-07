#!/usr/bin/env python
import time

class Timer(object):
   def __init__(self):
      self.timer_states = {}
      self.all_timers = {}

   def add_ID(self, ID, amount):
      #--this will add a new ID into the dictionaries, be wary of ID name choices, as they can be overwritten
      self.all_timers[ID] = amount
      self.timer_states[ID] = amount

   def countdown(self, ID, amount=None, countdown_speed=1, loop=False):
      #--will subtract 1 from the ID in the dictionary and return True if ID reaches 0 to imitate a real timer, can loop timer
      if ID not in self.all_timers:
         self.add_ID(ID, amount)

      if amount == None:
         amount = self.all_timers[ID]
      else:
         self.all_timers[ID] = amount
         if self.timer_states[ID] > amount:
            self.timer_states[ID] = amount

      self.timer_states[ID] -= countdown_speed
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

   def is_full(self, ID):
      return self.all_timers[ID] == self.timer_states[ID]

   def print_timer(self, ID):
      print('{}: {}'.format(ID, self.timer_states[ID]))

   def __iter__(self):
      for timer in self.all_timers.keys():
         yield timer
