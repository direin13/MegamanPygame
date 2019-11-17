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
      self.head = None

   def remove(self):
      #removes head from the list
      item = self.head.item
      self.head = self.head.next
      return item

   def clear(self):
      self.head = None

   def append(self, item):
      #adds to the linked list
         self.head = Node(item, self.head)

   def is_empty(self):
      return self.head == None

   def insert(self, item):
      #appends item to the end of the linked list
      if self.is_empty():
         self.append(item)

      else: #loop to the end and append another node
         ptr = self.head
         while ptr.next != None:
            ptr = ptr.next

         ptr.next = Node(item, None)

   def recursive_len(self, ptr):
      if ptr == None:
         return 0
      else:
         return 1 + self.recursive_len(ptr.next)

   def __len__(self):
      return self.recursive_len(self.head)


   def __str__(self):
      if self.is_empty():
         return '[]'
      else:
         return '[{}]'.format(self.head) #calls __str__ recursively on Nodes

   def __iter__(self):
      ptr = self.head
      while ptr != None:
         yield ptr.item
         ptr = ptr.next

   def link(self, other):
      #iterate to the end of 'other' and make the next node equal to a 'self.head', effectively combining the two lists
      #Note that 'other' will change become the combination of the two lists whereas 'self' will remain the unchanged
      if other.is_empty():
         other.head = self.head

      elif self.is_empty():
         self.head = other.head

      else:
         ptr = other.head
         while ptr.next != None:
            ptr = ptr.next
         ptr.next = Node(self.head.item, self.head.next)