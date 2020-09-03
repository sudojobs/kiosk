import pygame
from pygame import *
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN) #GPGPIO 14 -> IR sensor as input
GPIO.setup(24,GPIO.IN) #GPGPIO 14 -> IR sensor as input
path="/home/pi/kiosk/fabindia/"

running=True
clock_tick_rate=1
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

main_screen=pygame.image.load(path + 'fabindia.png')
pro1_screen=pygame.image.load(path + 'body.png')
pro2_screen=pygame.image.load(path + 'shampo.png')

def image_load(img,x,y):
    screen.blit(img, (x,y))

while running:
    # Did the user click the window close button?
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
               print("Quit")
               running = Falsei
    if(GPIO.input(24)==True):
       image_load(pro1_screen,0,0)
    elif (GPIO.input(23)==True):
       image_load(pro2_screen,0,0)
    else:    
       image_load(main_screen,0,0)
    
    pygame.display.flip()
    clock.tick(clock_tick_rate)
