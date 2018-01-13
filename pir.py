import RPi.GPIO as GPIO
import time
import vlc
import glob
import random
import subprocess
import os

PIR_OUT_PIN = 11    # pin11
random.seed(random.randint(0,420))
class Player:
    def __init__(self,directory):
        fileExp = directory + "/*.mp3"
        self.audioFiles=glob.glob(fileExp)
        self.numFiles = len(self.audioFiles)
        self.index = 0
    def playRandom(self):
        return
    def cleanUp(self):
        return

class vlcPlayer(Player):

    def __init__(self,directory):
        Player.__init__(self,directory)
        self.player = vlc.MediaPlayer()

    def playRandom(self):
        self.player = vlc.MediaPlayer(self.audioFiles[self.index])
        self.player.play()
        self.index += 1
        if self.index >= self.numFiles:
            self.index = 0
            random.shuffle(self.audioFiles)
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
        self.player = "play"
    def playRandom(self):
        FNULL = open(os.devnull, 'w')
        currentSong = self.audioFiles[self.index]
        command = self.player + " " + currentSong 
        print "Playing " + currentSong 
        self.pid = self.p.Popen("exec " + command, stdout=FNULL,stderr=subprocess.STDOUT,shell=True)  
        #subprocess.call( ["play",self.audioFiles[self.index]], stdout=FNULL,stderr=subprocess.STDOUT)
        self.index += 1
        if self.index >= self.numFiles:
            print "Reached the end of the files. Shuffling..."
            self.index = 0
            random.shuffle(self.audioFiles)
    def cleanUp(self):
        try:
            self.pid.terminate()
        except: 
            return
    def setPlayer(self,player):
        self.player = player

p = osPlayer("./audio")

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(PIR_OUT_PIN, GPIO.IN)    # Set BtnPin's mode is input

def destroy():
    p.cleanUp()
    GPIO.cleanup()                     # Release resource

def loop():
    while True:
        i = GPIO.input(PIR_OUT_PIN)
        if i == 0: 
            time.sleep(.01)
            pass
        elif i == 1:
            print 'Movement detected!'
            p.playRandom()
            time.sleep(9)
            print 'Ready to play again...'

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
