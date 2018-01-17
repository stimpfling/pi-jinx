import RPi.GPIO as GPIO
import time
import vlc
import glob
import random
import subprocess
import os
from datetime import datetime

# Some Global Variables 
PIR_OUT_PIN = 11    # pin11

class Player:
    def __init__(self,directory):
        fileExp = directory + "/*.mp3"
        self.audioFiles = glob.glob(fileExp)
        random.shuffle(self.audioFiles)
        self.numFiles = len(self.audioFiles)
        self.index = 0
    def getCurrentIndex(self):
        if self.index >= self.numFiles:
            self.index = 0
            random.shuffle(self.audioFiles)
        self.index += 1
        return self.index
    def playRandom(self):
        return
    def cleanUp(self):
        return

class vlcPlayer(Player):
    def __init__(self,directory):
        Player.__init__(self,directory)
        self.player = vlc.MediaPlayer()
    def playRandom(self):
        index = self.getCurrentIndex()
        currentSong = self.audioFiles[index]
        print "Playing " + currentSong
        self.player = vlc.MediaPlayer(currentSong)
        self.player.play()
    def release(self):
        self.player.release()
    def stop(self):
        self.player.stop()
    def cleanup(self):
        self.stop()
        self.release()
    
class osPlayer(Player):
    def __init__(self,directory):
        Player.__init__(self,directory)
        self.p = subprocess
        self.pid = -1
        # By default use the sox "play" cmd. Can use cvlc/whatever you have installed 
        self.player = "play"
    def playRandom(self):
        FNULL = open(os.devnull, 'w')
        index = self.getCurrentIndex()
        currentSong = self.audioFiles[index]
        command = self.player + " " + currentSong 
        print "Playing " + currentSong 
        self.pid = self.p.Popen("exec " + command, stdout=FNULL,stderr=subprocess.STDOUT,shell=True)  
    def cleanUp(self):
        try:
            self.pid.terminate()
        except: 
            return
    def setPlayer(self,player):
        self.player = player


def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(PIR_OUT_PIN, GPIO.IN)    # Set BtnPin's mode is input

def destroy():
    GPIO.cleanup()                     # Release resource

# Depends on declaration of player p
def loop():
    while True:
        i = GPIO.input(PIR_OUT_PIN)
        if i == 0: 
            # Having this small sleep cuts down drastically on CPU time 
            time.sleep(.01)
            pass
        elif i == 1:
            date = str(datetime.now()) 
            print 'Movement detected at ' + date
            p.playRandom()
            time.sleep(9)
            print 'Ready to play again...'

if __name__ == '__main__':     # Program start from here
    setup()
    random.seed(datetime.now())
    p = osPlayer("./audio")
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        p.cleanUp()
        destroy()
