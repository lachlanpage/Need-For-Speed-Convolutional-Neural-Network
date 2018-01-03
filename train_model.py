import h5py 
import numpy as np 
import tensorflow as tf 
from googlenet import googlenet
#from alexnet import alexnet

# Training Parameters
learning_rate = 0.001

WIDTH = 200
HEIGHT = 150
EPOCHS = 100
MODEL_NAME = "jatln-v0.3"


f = h5py.File("wasd_training_data.hdf5", "r")
print("File loaded")
model = googlenet(WIDTH, HEIGHT, learning_rate)

DATASET_COUNTER = 0 
for dataset in f.keys():
    DATASET_COUNTER+=1

DATASET_COUNTER = int(DATASET_COUNTER/2) 

for i in range(EPOCHS):

    for counter in range(DATASET_COUNTER):
        label_X = "dataset" + str(counter) + "_X"
        label_Y = "dataset" + str(counter) + "_Y"


        data_X = np.array(f[label_X])
        data_Y = np.array(f[label_Y])

        train_data_X = data_X[:-500].reshape(-1, WIDTH, HEIGHT, 3)
        train_data_Y = data_Y[:-500]

        test_data_X = data_X[-500:].reshape(-1, WIDTH, HEIGHT, 3)
        test_data_Y = data_Y[-500:]

        model.fit({'input' : train_data_X}, {'targets' : train_data_Y}, n_epoch = 1, validation_set=({'input': test_data_X}, {'targets': test_data_Y}), snapshot_step = 1000, show_metric=True, run_id=MODEL_NAME)
    if(i%5 == 0):
        model.save(MODEL_NAME)

    # tensorboard --logdir=/"beamng-car-model"
    #model.fit(X, Y, n_epoch=1000, validation_set=0.1, shuffle=True,
    #        show_metric=True, batch_size=64, snapshot_step=200,
    #        snapshot_epoch=False, run_id='googlenet_oxflowers17')
