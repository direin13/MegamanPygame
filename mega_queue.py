#!/usr/bin/env python

class Queue(object):

   def __init__(self, lst=None):
      if lst == None:
         self.lst = []
      else:
         self.lst = lst

   def enqueue(self, value):
      self.lst.append(value)

   def enqueue_start(self, value):
      self.lst = [value] + self.lst

   def dequeue(self):
      value = self.lst.pop(0)
      return value

   def enqueue_update(self, lst):
      self.lst.extend(lst)

   def enqueue_update_start(self, lst):
      self.lst = lst + self.lst

   def __str__(self):
      return '{}'.format(self.lst)
