#!/usr/bin/env python

class Stack(object):
   def __init__(self, lst=None):
      if lst == None:
         lst = []

      self.lst = lst

   def push(self, value):
      self.lst.append(value)

   def pop(self):
      return self.lst.pop()

   def is_empty(self):
      return len(self.lst) == 0

   def __str__(self):
      return '{}'.format(self.lst)