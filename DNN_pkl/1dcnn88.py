#%%
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
# from keras.layers import Activation, Reshape, Embedding
# from tensorflow.keras.layers import Conv1D, MaxPooling1D ,LSTM, CuDNNLSTM, BatchNormalization
from keras.layers import Conv1D, MaxPooling1D ,LSTM, BatchNormalization, GlobalAveragePooling1D
# from keras.callbacks import TensorBoard, EarlyStopping
from keras.utils import to_categorical
# from datetime import datetime
# import time
import matplotlib.pyplot as plt
import pickle
import numpy as np

TS_LENGTH = 92  # length of time series data
NUM_CLASS = 3   # 1,2,3 - (0 removed)


## use surs_obj.keys() to list the variables listed below - here 3 of them ##
with open("D:\\github\\time-series-dataset-augmentation\\wrkdir\\surs.pkl", "rb") as f:
    surs_obj = pickle.load(f)

# 1. single vector of numbers
sursclass=surs_obj['sursclass']
sursclass = np.array(sursclass)
sursclass = sursclass[:, np.newaxis] ; sursclass = sursclass.astype(np.int)

# 2. create list of file names from matlab cell array of strings
# [0] - only one array of strings and [i] entries
sursfile=surs_obj['sursfile']

# 3. create list of variable length arrays originally from matlab cell 
sursdata=surs_obj['sursdata']

del surs_obj # to free up memory

# create zeros of training data
Xtrg = np.zeros([len(sursdata),TS_LENGTH,3],np.int16)

# convert variable length into fixed length array
for i in range(len(sursdata)):
    #temp_data = sursdata[i] # take out a slice along row
    [dr, dc] = np.shape(sursdata[i])    
    if dr < TS_LENGTH:
        tdz = np.zeros([TS_LENGTH,3],dtype=np.int16)   # work matrix to insert
        tdz[:dr,:dc] = sursdata[i]        # overwrite
        Xtrg[i] = tdz
    else:
        Xtrg[i] = sursdata[i][0:TS_LENGTH]

Xtrg = np.float32(Xtrg)
#Xtrg = Xtrg *1.0/100 - 1.0 

mu = np.mean(Xtrg, axis=0)
sigma = np.std(Xtrg, axis=0)
Xtrg = (Xtrg - mu)/sigma

ytrg = to_categorical(sursclass-1, NUM_CLASS)

#dense_layers = [2]
layer_size = 44
#conv_layers = [4]

#            NAME = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
#            print(NAME)

model = Sequential()
            
model.add(Conv1D(layer_size, kernel_size=(7),activation='relu',input_shape=Xtrg.shape[1:]))
"""
model.add(Conv1D(100, 10, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(160, 8, activation='relu'))
model.add(Conv1D(160, 4, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(0.2))
model.add(Dense(NUM_CLASS, activation='softmax'))
"""
model.add(MaxPooling1D(pool_size=(1)))

#for a in range(conv_layer-1):
model.add(Conv1D(layer_size,kernel_size=(5), activation='relu'))
model.add(MaxPooling1D(pool_size=(1)))
model.add(Conv1D(layer_size,kernel_size=(3), activation='relu'))
model.add(MaxPooling1D(pool_size=(1)))
#model.add(Conv1D(layer_size,kernel_size=(3), activation='relu'))
#model.add(MaxPooling1D(pool_size=(1)))
            
model.add(Flatten())
            
model.add(Dense(120, activation='relu'))
model.add(Dropout(0.1)) 
model.add(Dense(120, activation='relu'))
model.add(Dropout(0.1))
            
model.add(Dense(NUM_CLASS, activation='softmax')) # was dense(3)
#tensorboard = TensorBoard(log_dir="C:\\tmp\\logs\\example\\{}".format(NAME))
#earlystopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', patience=2)
            
#model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
            
adam = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)
#adam = tf.keras.optimizers.Adam(lr=0.001)
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

print(model.summary())
            
#model.fit(Xtrg, ytrg, batch_size=20, epochs=40, validation_split=0.2, verbose=1, callbacks=[tensorboard])
history=model.fit(Xtrg, ytrg, batch_size=10, epochs=35, validation_split=0.1, verbose=1)
plt.plot(history.history['accuracy'], label='accuracy')
            
model.save('D:/tmp/AAFT70Conv1D_88_py.model')
            
print("Run the command line on anaconda prompt:\n" \
          "--> tensorboard --logdir=/tmp/logs/ --host localhost --port 8088 " \
          "\nThen open http://localhost:8088/ into your web browser")


# %%
