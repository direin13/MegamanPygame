import pygame
from bit_text import Bit_text
from timer import Timer
import sys
clock = pygame.time.Clock()

s = input()

screen = pygame.display.set_mode((600,600))

run = True

text = Bit_text(s, 600, 250, 4, 4, pattern_interval=40)
text2 = Bit_text(s, 130, 250, 4, 4, pattern_interval=15, colour=(0,0,0))
myt = Timer()
myt.add_ID('inc', 5)

while run:
   screen.fill((0,0,0))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         run = False

   keys = pygame.key.get_pressed()
   if True in [keys[pygame.K_RIGHT], keys[pygame.K_LEFT], keys[pygame.K_UP], keys[pygame.K_DOWN]] and myt.is_finished('inc') != True:
      myt.countdown('inc')
   elif myt.is_finished('inc'):
      myt.replenish_timer('inc')

      if keys[pygame.K_RIGHT]:
         text.width += 1
      elif keys[pygame.K_LEFT]:
         text.width -= 1
      if keys[pygame.K_UP]:
         text.height -= 1
      elif keys[pygame.K_DOWN]:
         text.height += 1

   text.x -= 2

   dist = 6
   size = 0

   text2.x, text2.y, text2.width, text2.height = text.x-dist, text.y+dist, text.width+size, text.height+size

   text2.display(screen)
   text.display(screen, 'flash')
   print(text.width, text.height)
   pygame.display.update()
   clock.tick(60)