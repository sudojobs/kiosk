import commands
import re
import sys, os
import time
import glob
import shutil
import RPi.GPIO as GPIO
import subprocess

MOUNT_DIR  = "/mnt/usb_stick"
USB_FILE = MOUNT_DIR + "/"
MEDIA_FILE = glob.glob('/home/pi/video/*')
media_file = '/home/pi/video/'
MEDIA_PATH = "/home/pi/video"
white = (255, 255, 255) 
green = (100, 255, 255) 
blue  = (0, 0, 128)
black = (0,0,0)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN) #GPGPIO 14 -> IR sensor as input
GPIO.setup(24,GPIO.IN) #GPGPIO 14 -> IR sensor as input

global playprocess
# assigning values to X and Y variable 
X = 400
Y = 400

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Enable print
def enablePrint():
    sys.stdout = sys.__stdout__

def run_command(command):
    ret_code, output = commands.getstatusoutput(command)
    if ret_code == 1:
        raise Exception("FAILED: %s" % command)
    return output.splitlines() 

blockPrint()
import pygame
enablePrint()
pygame.init()

# Set up the drawing window
#screen = pygame.display.set_mode([500, 500])
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
font = pygame.font.Font('freesansbold.ttf', 32) 
insert = font.render('Looking for USB Drive', True, green, white) 
copy   = font.render('Copy files from USB Drive', True, green, white) 
#state=1 pendrive check mode
#state=2 pendrive content copy mode
#state=3 playlist creation mode
#state=4 normal operation of display
#state=5 exit mode

state=1
usb_present=0
main_play=""
pro1_play=""
pro2_play=""
main_content=0
pro1_content=0
pro2_content=0
main_screen=""
pro1_screen=""
pro2_screen=""
omx=0
def content_check(file_name):
    e=file_name[2:]
    n=file_name[0]
    if(e=="png" or e=="jpg"):
       return 1
    else:
       return 0

def image_load(img,x,y):
    screen.blit(img, (x,y))

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if(state==1):
      # Fill the background with white
      screen.fill(white)
      screen.blit(insert, (100,240))
      output = run_command("blkid | grep LABEL | grep -v boot")
      for x in output:
          p=x.split()
          tmp=re.compile(r'/dev/sd*')
          match=tmp.search(p[0])
          if(match!=None):
             usb_present=1
             uidf=x.split()
             uids=uidf[2].split("=")
             command = "mount --uuid %s %s" % (uids[1], MOUNT_DIR)
             run_command(command)
          state=2
    elif(state==2):
      if(usb_present==1):  
         files=os.listdir(USB_FILE)
         if ('System Volume Information') in files:
              files.remove('System Volume Information')
         for f in MEDIA_FILE:
            os.remove(f)
         screen.fill(white)
         screen.blit(copy, (50,240))
         for f in files:
            file_path=MOUNT_DIR +"/" + f
            target_path=MEDIA_PATH + "/" + f
            shutil.copyfile(file_path,target_path) 
      state=3
    elif(state==3):
      screen.fill(black)
      player_files = os.listdir(MEDIA_PATH)
      for f in player_files:
          num=f[0]
          if(num=="1"):
              main_content=(content_check(f))
              main_play=f
              main_screen=(media_file +  main_play)
          elif(num=="2"):
              pro1_content=(content_check(f))
              pro1_play=f
              pro1_screen=(media_file +  pro1_play)
          elif(num=="3"):    
              pro2_content=(content_check(f))
              pro2_play=f
              pro2_screen=(media_file +  pro2_play)
      state=4
    elif(state==4):
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
             state=5
          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_q:
                state=5    
      if(GPIO.input(24)==True):
        if(pro1_content):
           subprocess.call(['pkill', '-9', 'omxplayer']) 
           pro1_img=pygame.image.load(pro1_screen)
           image_load(pro1_img,0,0)
        else:
           if(omx==1):
              print(" I am here")
              subprocess.call(['pkill', '-9', 'omxplayer']) 
              playprocess=subprocess.call(['omxplayer','--no-osd','--no-keys','-b','-o','hdmi',pro1_screen,">/dev/null 2>&1>"],stdin=subprocess.PIPE,stdout=open(os.devnull, 'wb') )
              omx=0
           #poll1 = p1.poll()
           #if poll1 != None:
           #   omx=0 
      elif (GPIO.input(23)==True):
          omx=0 
          if(pro2_content):
             subprocess.call(['pkill', '-9', 'omxplayer']) 
             pro2_img=pygame.image.load(pro2_screen)
             image_load(pro2_img,0,0)
          else:
             if(omx==0):
                subprocess.call(['pkill', '-9', 'omxplayer']) 
                playprocess=subprocess.call(['omxplayer','--no-osd','--no-keys','-b','-o','hdmi',pro2_screen,">/dev/null 2>&1>"],stdin=subprocess.PIPE,stdout=open(os.devnull, 'wb') )
                omx=0
            # poll2 = p2.poll()
            # if poll2 != None:
            #    omx=0 
      else:    
          if(main_content):
             subprocess.call(['pkill', '-9', 'omxplayer']) 
             main_img=pygame.image.load(main_screen)
             image_load(main_img,0,0)
          else: 
             if(omx==0):
                subprocess.call(['pkill', '-9', 'omxplayer']) 
                playprocess=subprocess.Popen(['omxplayer','--no-osd','--no-keys','-b','-o','hdmi',main_screen,">/dev/null 2>&1>"],stdin=subprocess.PIPE,stdout=open(os.devnull, 'wb') )
                omx=1
             poll = playprocess.poll()
             if poll != None:
                omx=0
    else:    
         running=False
         subprocess.call(['pkill', '-9', 'omxplayer']) 
         #pygame.quit()
         break
pygame.display.flip()
