#!/usr/bin/env python
from linkedlist import *

class Stack(object):

   def __init__(self):
      self.lst = LinkedList()

   def push(self, item):
      self.lst.add(item)

   def push_start(self, item):
      #insert to the beginning of stack
      self.lst.append(item)

   def pop(self):
      item = self.lst.remove()
      return item

   def push_update(self, other):
      #will link 'other' to 'self' effectively mimicking list.extend(), see linkedlist.LinkedList.link for more
      other.lst.link(self.lst)

   def push_update_start(self, other):
      #push a list to beginning of stack
      for item in lst:
         self.lst.append(item)

   def is_empty(self):
      return self.lst.is_empty()

   def clear(self):
      self.lst.clear()

   def __iter__(self):
      while self.lst.is_empty() != True:
         yield self.pop()

   def __len__(self):
      return len(self.lst)

   def __str__(self):
      return '{}'.format(self.lst)