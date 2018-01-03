#Collect CNN data using HDF5 format
from PIL import ImageGrab
from PIL import Image
import numpy as np
import h5py
import cv2
import time
import win32api
import scipy.misc

#Key Presses Available 
W =   [1,0,0,0,0]
A =   [0,1,0,0,0]
S =   [0,0,1,0,0]
D =   [0,0,0,1,0]

def key_check(): 
    #Uses Win32API to get key state from keyboard
    #Returns the appropriate key list 
    if(win32api.GetAsyncKeyState(ord('W'))):
        return W 
    elif(win32api.GetAsyncKeyState(ord('A'))):
        return A 
    elif(win32api.GetAsyncKeyState(ord('S'))):
        return S 
    elif(win32api.GetAsyncKeyState(ord('D'))):
        return D
    elif(win32api.GetAsyncKeyState(ord('P'))):
        return 'P'
    elif(win32api.GetAsyncKeyState(ord('U'))):
        return 'U'
    else:
        return NK 

def save_data(balanced_data):
    X_data = []
    Y_data = []
    for row in balanced_data:
        X_data.append(row[0]) 
        Y_data.append(row[1])

    print("saving hdf5 data...")
    f = h5py.File("wasd_training_data.hdf5", "a")

    DATASET_COUNTER = 0 
    for dataset in f.keys():
        DATASET_COUNTER+=1

    DATASET_COUNTER = int(DATASET_COUNTER/2)
    label_X = "dataset" + str(DATASET_COUNTER) + "_X"
    label_Y = "dataset" + str(DATASET_COUNTER) + "_Y"

    print(label_X, label_Y)

    dsetX = f.create_dataset(label_X, data=X_data)
    dsetY = f.create_dataset(label_Y, data = Y_data)
                
    f.close()
    print("file saved")

def balance_data(unbalanced_data):
    W_list = []
    A_list = []
    S_list = []
    D_list = []

    for row in unbalanced_data: 
        if(row[1] == W):
            W_list.append(row)
        elif(row[1] == A):
            A_list.append(row)
        elif(row[1] == S):
            S_list.append(row)
        elif(row[1] == D):
            D_list.append(row)
        else: 
            print("ERROR")

    #Get min data source 
    print(len(W_list),len(A_list),len(S_list),len(D_list))

    W_list = W_list[:len(A_list)][:len(D_list)]
    A_list = A_list[:len(W_list)]
    D_list = D_list[:len(W_list)]
    S_list = S_list[:len(W_list)]
    NK_list = NK_list[:len(W_list)]

    print("FInishied sorting") 

    print(len(W_list),len(A_list), len(S_list), len(D_list))

    final_data = np.concatenate([W_list,A_list,S_list, D_list])

    return final_data

#Countdown to get environment set up before running :) 
def start_countdown():
    COUNTDOWN_LENGTH = 5
    for i in range(COUNTDOWN_LENGTH):
        print(COUNTDOWN_LENGTH-i)
        time.sleep(1)
    print("Data Capture Starting...")
training_data = []

WIDTH = 800 
HEIGHT = 600
file_exists = False
#ImageGrab Coordinates 
UL_X = 3
UL_Y = 26
LR_X = UL_X+800
LR_Y = UL_Y+600

IMG_LIST = []
KEY_PRESSED_LIST = []

start_countdown() 
while(True):
    #Control C to exit loop -> need to fix this 
    img = ImageGrab.grab(bbox=(UL_X,UL_Y, LR_X, LR_Y))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = scipy.misc.imresize(img, [150,200])

    key_pressed = key_check()
    if(key_pressed != 'P' and key_pressed != 'U' and key_pressed!=NK):
        #Append key presses
        IMG_LIST.append(img)
        KEY_PRESSED_LIST.append(key_pressed)
        training_data.append([img, key_pressed])
        print(len(training_data))

        #Save data every 25,000 training samples collected
        if(len(training_data) % 25000 == 0):
            print("saving data")
            print("Balancing Data") 

            now = time.time()
            balanced_data = balance_data(training_data)
            finished_time = time.time()

            print("Data Balanced")
            print ("time taken: " + str(finished_time - now))
            print(len(balanced_data))

            save_data(balanced_data)
            training_data.clear()
    else: 
        paused = True
        print("Data collection Paused")
        while paused: 
            key_pressed = key_check() 
            if(key_pressed == 'U'):
                paused = False 


