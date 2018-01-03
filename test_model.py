from googlenet import googlenet
from alexnet import alexnet
from PIL import ImageGrab
from PIL import Image
import numpy as np 
import pyautogui 
import cv2
import time
import random 
import win32api
import scipy.misc
import time 

#Key Presses Available 
W =   [1,0,0,0,0]
A =   [0,1,0,0,0]
S =   [0,0,1,0,0]
D =   [0,0,0,1,0]
NK =  [0,0,0,0,1]
#Used because CNN responds to quickly to be natural
DELAY_FACTOR = 0.2

def w(): 
    pyautogui.keyDown('w')
    pyautogui.keyUp('d')
    pyautogui.keyUp('a')
    pyautogui.keyUp('s')

def s(): 
    pyautogui.keyDown('s')
    pyautogui.keyUp('d')
    pyautogui.keyUp('a')
    pyautogui.keyUp('w')

def a(): 
    #Random mutation to move forward while 'a' is pressed
    #Helps with movement by CNN
    if random.randrange(0,3) == 1:
        pyautogui.keyDown('w')
    else:
        pyautogui.keyUp('w')
    pyautogui.keyDown('a')
    pyautogui.keyUp('d')
    pyautogui.keyUp('w')
    pyautogui.keyUp('s')

def d():
    if random.randrange(0,3) == 1:
        pyautogui.keyDown('w')
    else:
        pyautogui.keyUp('w')
    pyautogui.keyDown('d')
    pyautogui.keyUp('w')
    pyautogui.keyUp('s')
    pyautogui.keyUp('a')

def nk():
    if random.randrange(0,3) == 1:
        pyautogui.keyDown('w')
    elif(random.randrange(0,3) == 2):
        pyautogui.keyDown('s')
        time.sleep(0.5)
        pyautogui.keyUp('s')
    else:
        pyautogui.keyUp('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('d')
    pyautogui.keyUp('s')

#Model Parameters
WIDTH = 200
HEIGHT = 150
EPOCHS = 3
learning_rate = 0.001
MODEL_NAME = "model_alexnet-14131"
model = alexnet(WIDTH, HEIGHT, learning_rate) 
model.load(MODEL_NAME) 
print("model loaded successfully")

UL_X = 3
UL_Y = 26
LR_X = UL_X+800
LR_Y = UL_Y+600

paused = False 
while(True):
    if not paused: 
        img = ImageGrab.grab(bbox=(UL_X,UL_Y, LR_X, LR_Y))
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #resize 256x256 for more efficient space 
        img = scipy.misc.imresize(img, [150,200])

        prediction = model.predict([img.reshape(WIDTH, HEIGHT, 3)])[0]
        #np.array is smoothing coefficients to help with smoother state transitions
        prediction = np.array(prediction) * np.array([4.5, 0.1, 0.1, 0.1, 0.2])

        #Thresholding cutoffs for predictions
        minIndex = np.argmax(prediction)
        turn_thresh = 1
        fwd_thresh = 0.7
        if(minIndex == 0):
            print("Forward")
            w() 
        if(minIndex == 1): 
            print("Left")
            a() 
        if(minIndex == 2):
            print("Back")
            s() 
        if(minIndex == 3): 
            print("Right")
            d() 
        if(minIndex == 4):
            print("no Key")
            nk()

    #Press T to pause CNN and reposition car if neccessary 
    if(win32api.GetAsyncKeyState(ord('T'))):
        print("CNN Paused")
        if paused:
            paused = False 
            time.sleep(5) 
        else: 
            pyautogui.keyUp('s')
            pyautogui.keyUp('a')
            pyautogui.keyUp('w')
            pyautogui.keyUp('d')
            paused = True
