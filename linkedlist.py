#!/usr/bin/env python

class Node(object):
   def __init__(self, item, next=None):
      self.item = item
      self.next = next

   def __str__(self):
      if self.next == None:
         return '{}'.format(self.item)
      else:
         return '{}, {}'.format(self.next, self.item)


class LinkedList(object):
   def __init__(self):
      self.tail = None

   def remove(self):
      #removes tail from the list
      item = self.tail.item
      self.tail = self.tail.next
      return item

   def clear(self):
      self.tail = None

   def append(self, item):
      #append to the end of a linked list
         self.tail = Node(item, self.tail)

   def is_empty(self):
      return self.tail == None

   def insert(self, item):
      #appends item to the head of the linked list
      if self.is_empty():
         self.append(item)
      else:
         ptr = self.tail
         while ptr.next != None:
            ptr = ptr.next

         ptr.next = Node(item, None)

   def recursive_len(self, ptr):
      if ptr == None:
         return 0
      else:
         return 1 + self.recursive_len(ptr.next)

   def __len__(self):
      return self.recursive_len(self.tail)


   def __str__(self):
      if self.is_empty():
         return '[]'
      else:
         return '[{}]'.format(self.tail) #calls __str__ recursively on Nodes

   def __iter__(self):
      ptr = self.tail
      while ptr != None:
         yield ptr.item
         ptr = ptr.next

   def link(self, other):
      #iterate to the end of 'other' and make the next node equal to a 'self.tail', effectively combining the the lists with minimal effort
      #Note that 'other' will change become the combination of the two lists whereas 'self' will remain the unchanged
      if other.is_empty():
         other.tail = self.tail

      elif self.is_empty():
         self.tail = other.tail

      else:
         ptr = other.tail
         while ptr.next != None:
            ptr = ptr.next
         ptr.next = Node(self.tail.item, self.tail.next)
