#!/usr/bin/env python
import time

class Timer(object):
   """used to replicate time within a loop"""
   def __init__(self):
      self.all_timers = {}
      self.loop_states = {}

   def add_ID(self, ID, amount):
      """adds a reference to ID to keep track of timer.
         Amount is the amount of frames the ID can be active for"""
      self.all_timers[ID] = {'origin': amount, 'curr_state': amount}
      self.loop_states[ID] = {'origin': 1, 'curr_state':1}
      return self

   def _increment_loop_state(self, ID, loop_amount=-1):
      """Increments loop state. Shouldn't be done manually unless
         you want manually skip a loop"""
      if loop_amount == -1: #loop infiniteley
         self.all_timers[ID]['curr_state'] = self.all_timers[ID]['origin']

      else: #count up until reached loop amount
         if self.loop_states[ID]['curr_state'] >= self.loop_states[ID]['origin']:
            self.all_timers[ID]['curr_state'] = 0
         else:
            self.loop_states[ID]['curr_state'] += 1
            self.all_timers[ID]['curr_state'] = self.all_timers[ID]['origin']

      return self
      

   def countdown(self, ID, amount=None, countdown_speed=1, loop=False, loop_amount=-1):
      """Counts down an ID. Amount is the number of frames to countdown until timer ID is
         finished. If ID doesn't exist, it will be added automatically.
         Loop parameter will automatically restart the counter upon finish. If loop is True
         then by default it will loop forever."""
      if ID not in self.all_timers:
         self.add_ID(ID, amount)

      if amount != None:
         self.all_timers[ID]['origin'] = amount
         if self.all_timers[ID]['curr_state'] > amount:
            self.all_timers[ID]['curr_state'] = amount

      self.all_timers[ID]['curr_state'] -= countdown_speed

      if loop_amount != -1 and loop_amount != self.loop_states[ID]['origin']: #if loop amount has changed
         self.loop_states[ID]['origin'] = loop_amount

      if self.all_timers[ID]['curr_state'] < 0:
         if loop == False:
            self.all_timers[ID]['curr_state'] = 0
         else:
            self._increment_loop_state(ID, loop_amount)

      return self


   def replenish_timer(self, ID, new_amount=None):
      if new_amount == None:
         self.all_timers[ID]['curr_state'] = self.all_timers[ID]['origin']
      else:
         self.all_timers[ID]['origin'] = new_amount
         self.all_timers[ID]['curr_state'] = new_amount
      self.loop_states[ID]['curr_state'] = 1

      return self


   def get_ID(self, ID):
      """returns dict of info about ID"""
      return self.all_timers[ID]


   def get_loop_states(self, ID):
      return self.loop_states[ID]


   def is_finished(self, ID, include_loop=False):
      """returns true if the ID has counted down to 0.
         If include_loop is True, the function will only
         return true if ID has looped completely as well."""
      if include_loop:
         return self.all_timers[ID]['curr_state'] <= 0 and self.loop_states[ID]['curr_state'] >= self.loop_states[ID]['origin']
      else:
         return self.all_timers[ID]['curr_state'] <= 0


   def is_almost_finished(self, ID, n):
      """Will return true if the state of an ID timer
         has reached or is less than n"""
      return (self.all_timers[ID]['curr_state'] - n) <= 0


   def is_full(self, ID):
      return self.all_timers[ID]['origin'] == self.all_timers[ID]['curr_state']


   def print_ID(self, ID):
      print('{}: timer_state = {}::{}, loop_state = {}::{}'.format(ID, 
                                                                   self.all_timers[ID]['origin'], 
                                                                   self.all_timers[ID]['curr_state'], 
                                                                   self.loop_states[ID]['origin'], 
                                                                   self.loop_states[ID]['curr_state']
                                                                  )
           )

   def __str__(self):
      a = []
      for ID in self:
         a.append('{}: timer_state = {}::{}, loop_state = {}::{}'.format(ID, 
                                                                         self.all_timers[ID]['origin'], 
                                                                         self.all_timers[ID]['curr_state'], 
                                                                         self.loop_states[ID]['origin'], 
                                                                         self.loop_states[ID]['curr_state']
                                                                        )
                 )
      return '\n'.join(a)

   def __iter__(self):
      for timer_name in self.all_timers.keys():
         yield timer_name
