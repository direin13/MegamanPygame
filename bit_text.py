#!/usr/bin/env python
import pygame

#used to display text in 8 bit style

# list[i] = y pos, list[i][j] = x pos 
letters = { '.': [[], [], [], [], [], [0, 1], [0, 1]],
            '(': [[3, 4, 5], [1, 2], [0, 1], [0], [0, 1], [1, 2], [3, 4, 5]],
            ',': [[], [], [], [3, 4], [3, 4], [4], [3]],
            '-': [[], [], [], [0, 1, 2, 3, 4, 5, 6], [], [], []],
            ':': [[3, 4], [3, 4], [], [], [], [3, 4], [3, 4]],
            '0': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 4, 5, 6], [0, 1, 3, 5, 6], [0, 1, 2, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            '1': [[2, 3, 4], [1, 2, 3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4]],
            '2': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [5, 6], [3, 4, 5], [1, 2], [0, 1], [0, 1, 2, 3, 4, 5, 6]],
            '3': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [5, 6], [2, 3, 4, 5], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            '4': [[0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 2, 3, 4, 5, 6], [4, 5], [4, 5]],
            '5': [[0, 1, 2, 3, 4, 5, 6], [0, 1], [0, 1, 2, 3, 4, 5], [5, 6], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            '6': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1], [0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            '7': [[0, 1, 2, 3, 4, 5, 6], [5, 6], [4, 5], [3, 4], [2, 3, 4], [2, 3, 4], [2, 3, 4]],
            '8': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            '9': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5, 6], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            'a': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
            'c': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1], [0, 1], [0, 1], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            'd': [[0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5]],
            'e': [[0, 1, 2, 3, 4, 5, 6], [0, 1], [0, 1], [0, 1, 2, 3, 4, 5], [0, 1], [0, 1], [0, 1, 2, 3, 4, 5, 6]],
            'i': [[3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4]],
            'h': [[0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
            'm': [[0, 1, 5, 6], [0, 1, 2, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6], [0, 1, 3, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
            'n': [[0, 1, 5, 6], [0, 1, 2, 5, 6], [0, 1, 2, 3, 5, 6], [0, 1, 3, 4, 5, 6], [0, 1, 4, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6]],
            'o': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            'p': [[0, 1, 2, 3, 4, 5], [0, 1, 5, 6,], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5], [0, 1], [0, 1]],
            'r': [[0, 1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 2, 3, 4, 5], [0, 1, 4, 5], [0, 1, 5, 6]],
            's': [[1, 2, 3, 4, 5], [0, 1, 5, 6], [0, 1], [1, 2, 3, 4, 5], [5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            't': [[0, 1, 2, 3, 4, 5, 6], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4], [3, 4]],
            'u': [[0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [0, 1, 5, 6], [1, 2, 3, 4, 5]],
            'y': [[0, 1, 4, 5], [0, 1, 4, 5], [0, 1, 4, 5], [1, 2, 3, 4], [2, 3], [2, 3], [2, 3]],
            ' ': [[], [], [], [], [], [], []]}

def display_text(surf, coordinates, string, width=1, height=1, colour=(255,255,255)):
   global letters

   all_chars = list(string)
   pos = 0 #the offeset where character will be drawn

   for char in all_chars:
      y = coordinates[1]
      for array in letters[char.lower()]: # going through every array in characters and making a rectangle at each number in the array
         if len(array) != 0:
            for i in range(len(array)):
               x = coordinates[0] + (array[i] * width) + pos
               pygame.draw.rect(surf, colour, (x, y, width, height))
         y += 1 * height
      pos += 8 * width


