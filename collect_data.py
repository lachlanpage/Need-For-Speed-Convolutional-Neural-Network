#Simple script to collect the training data used for the neural network 


from PIL import ImageGrab
from PIL import Image
import numpy as np
import cv2
import time
import win32api
import scipy.misc

#Key Presses Available 
WA =[1,0,0,0,0,0,0,0,0]
SA =[0,1,0,0,0,0,0,0,0]
WD =[0,0,1,0,0,0,0,0,0]
SD =[0,0,0,1,0,0,0,0,0]
W  =[0,0,0,0,1,0,0,0,0]
A  =[0,0,0,0,0,1,0,0,0]
S  =[0,0,0,0,0,0,1,0,0]
D  =[0,0,0,0,0,0,0,1,0]
NK =[0,0,0,0,0,0,0,0,1]

def key_check(): 
    #Uses Win32API to get key state from keyboard
    #Returns the appropriate key list 
    if(win32api.GetAsyncKeyState(ord('A')) and win32api.GetAsyncKeyState(ord('W'))):
        return WA 

    elif(win32api.GetAsyncKeyState(ord('A')) and win32api.GetAsyncKeyState(ord('S'))):
        return SA 

    elif(win32api.GetAsyncKeyState(ord('D')) and win32api.GetAsyncKeyState(ord('W'))):
        return WD

    elif(win32api.GetAsyncKeyState(ord('D')) and win32api.GetAsyncKeyState(ord('S'))):
        return SD

    elif(win32api.GetAsyncKeyState(ord('W'))):
        return W 

    elif(win32api.GetAsyncKeyState(ord('A'))):
        return A 

    elif(win32api.GetAsyncKeyState(ord('S'))):
        return S 

    elif(win32api.GetAsyncKeyState(ord('D'))):
        return D
    else:
        return NK 


#Countdown to get environment set up before running
COUNTDOWN_LENGTH = 5
for i in range(COUNTDOWN_LENGTH):
    print(COUNTDOWN_LENGTH-i)
    time.sleep(1)
print("Data Capture Starting...")

training_data = []


#ImageGrab Coordinates 
UL_X = 640 
UL_Y = 300 

LL_X = 640+640 
LL_Y = 300+480

while(True):
    #Control C to exit loop -> need to fix this 
    img = ImageGrab.grab(bbox=(UL_X,UL_Y, LL_X, LL_Y))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #resize 256x256 for more efficient space 
    img = scipy.misc.imresize(img, [256,256])

    key_pressed = key_check()
    training_data.append([img, key_pressed])

    print(len(training_data))
    if(len(training_data) % 10000 == 0):
        print("data saved")
        np.save("training_data.npy", training_data)



