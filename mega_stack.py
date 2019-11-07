#!/usr/bin/env python
from linkedlist import *

class Stack(object):

   def __init__(self):
      self.lst = LinkedList()

   def push(self, item):
      self.lst.append(item)

   def push_start(self, item):
      #append to the beginning of queue
      self.lst.insert(item)

   def pop(self):
      item = self.lst.remove()
      return item

   def push_update(self, other):
      #will link 'other' to 'self' effectively mimicking list.extend(), see linkedlist.LinkedList.link for more
      other.lst.link(self.lst)

   def push_update_start(self, other):
      #update to beginning of queue
      for item in lst:
         self.lst.insert(item)

   def is_empty(self):
      return self.lst.is_empty()

   def clear(self):
      self.lst.clear()

   def __str__(self):
      return '{}'.format(self.lst)