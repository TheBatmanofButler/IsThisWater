#!/usr/bin/env python
# coding: utf-8

# ## Source: https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html

# In[1]:


from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K

import os
import math
import random
import shutil


# In[2]:


LABELED_IMAGES_DIRECTORY = '../static/labeled_images/'

WATER_DIRECTORY = os.path.join(LABELED_IMAGES_DIRECTORY, 'water')
NO_WATER_DIRECTORY = os.path.join(LABELED_IMAGES_DIRECTORY, 'no_water')

TRAIN_IMAGES_DIRECTORY = '../model_data/train'
VAL_IMAGES_DIRECTORY = '../model_data/val'
TEST_IMAGES_DIRECTORY = '../model_data/test/test_images'

total_num_water_images = len([name for name in os.listdir(WATER_DIRECTORY)])
total_num_no_water_images = len([name for name in os.listdir(NO_WATER_DIRECTORY)])

print(total_num_water_images, 'total images of water')
print(total_num_no_water_images, 'total images of no water')


# In[3]:


num_water_samples = total_num_water_images - total_num_water_images  % 40
num_no_water_samples = total_num_no_water_images - total_num_no_water_images % 40

print(num_water_samples, 'images of water used')
print(num_no_water_samples, 'images of no water used')


# In[4]:


# dimensions of our images.
img_width, img_height = 1000, 1000
batch_size = 20
epochs = 1

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


# In[5]:


def copy_image_subset(filenames, target_directory, file_indices, label):
    for ind in file_indices:
        filename = filenames[ind]
        current_filepath = os.path.join(LABELED_IMAGES_DIRECTORY, label, filename)        
        target_filepath = os.path.join(target_directory, label, filename)

        shutil.copyfile(current_filepath, target_filepath)


# In[6]:


def move_images_to_model_dirs(directory, label, num_samples):
    
    global total_train_samples
    global total_val_samples
    
    filenames = os.listdir(directory)[:num_samples]
    all_file_indices = list(range(num_samples))
    random.shuffle(all_file_indices)

    num_train_samples = math.floor(num_samples * 0.5)
    train_sample_indices = all_file_indices[:num_train_samples]
    val_sample_indices = all_file_indices[num_train_samples:]

    total_train_samples += len(train_sample_indices)
    total_val_samples += len(val_sample_indices)

    copy_image_subset(filenames, TRAIN_IMAGES_DIRECTORY, train_sample_indices, label)
    copy_image_subset(filenames, VAL_IMAGES_DIRECTORY, val_sample_indices, label)


# In[7]:


labeled_directories = [(WATER_DIRECTORY, 'water'),
                       (NO_WATER_DIRECTORY, 'no_water')]

total_train_samples = 0
total_val_samples = 0

move_images_to_model_dirs(WATER_DIRECTORY, 'water', num_water_samples)
move_images_to_model_dirs(NO_WATER_DIRECTORY, 'no_water', num_no_water_samples)

print('Total images for training:', total_train_samples)
print('Total images for validation:', total_val_samples)


# In[8]:


model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])


# In[9]:


# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_IMAGES_DIRECTORY,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

val_generator = test_datagen.flow_from_directory(
    VAL_IMAGES_DIRECTORY,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')


# In[ ]:


model.fit_generator(
    train_generator,
    steps_per_epoch=total_train_samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=total_val_samples // batch_size)

model.save_weights('weights.h5')


# In[ ]:


# model.evaluate_generator(generator=test_generator)

