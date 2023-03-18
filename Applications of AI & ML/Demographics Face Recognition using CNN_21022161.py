#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########################################
# Demographics Face Recognition using CNN #
###########################################

#libraries used
import numpy as np 
import pandas as pd 
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow.keras.utils import to_categorical
from PIL import Image
from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPool2D, GlobalMaxPool2D, Dropout
from tensorflow.keras.optimizers import SGD
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import math

# About Dataset
# UTKFace dataset is a large-scale face dataset with long age span (range from 0 to 116 years old). 
# The dataset consists of over 20,000 face images with annotations of age, gender, and ethnicity. 
# The images cover large variation in pose, facial expression, illumination, occlusion, resolution, etc.
# Kaggle url for the dataset : https://www.kaggle.com/datasets/jangedoo/utkface-new
# This dataset serves as a baseline for face pictures and includes noise, lighting, posing, and looks, among other real-world imaging scenarios.
# The labels of each face image is embedded in the file name, formated like [age][gender][race]_[date&time].jpg
# For gender, 0 indicate male and 1 indicate female
# For race, 0 indicate White, 1 indicate black, 2 indicate Asian, 3 indicate Indian and 4 indicate Other races

#Exploratory data analysis
Dataset_path = "/Users/macbook/Downloads/Course work/Applications of AI & ML/UTKFace"
Train_Test_Split = 0.8
Img_Width = 198
Img_Height = 198
ID_Gender_Map = {0: 'male', 1: 'female'}
Gender_ID_Map = dict((i, j) for j, i in ID_Gender_Map.items())
ID_Race_Map = {0: 'white', 1: 'black', 2: 'asian', 3: 'indian', 4: 'others'}
Race_ID_Map = dict((i, j) for j, i in ID_Race_Map.items())  


#This function will be used to iterate over each file of the UTK dataset and returns 
#required attributes such as age,gender and race for further action.
#IF any invalid file names found,it will catch in the exception part and display it
def parse_file_path(file_path):
    try:
        path, file_name = os.path.split(file_path)
        file_name, extension = os.path.splitext(file_name)
        age, gender, race, _ = file_name.split("_")
        return int(age), ID_Gender_Map[int(gender)], ID_Race_Map[int(race)]
    except Exception as e:
        print(file_path)
        return None, None, None

#Creating pandas data frame of age, gender,race and images
files = glob.glob(os.path.join(Dataset_path, "*.jpg"))
attributes = list(map(parse_file_path, files))
df = pd.DataFrame(attributes)
df['file'] = files
df.columns = ['age', 'gender', 'race', 'file']
#Eliminating null values
df = df.dropna()
print(df.head())


#Basic details of the dataframe
df.describe()
df.info()


#We can now use graphs to evaluate the data and gain a better grasp of its distribution and other properties.

ages = df['age']
nbins = 10
plt.hist(ages,nbins,color='lightblue',histtype='bar')
plt.show()
# Could see that the majority of the population is between the age group 20 to 30.

sns.countplot(x='gender', data=df);
plt.show()
#Both male and female count are over 2k

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
sns.boxplot(data=df, x='gender', y='age', ax=ax1)
sns.boxplot(data=df, x='race', y='age', ax=ax2)
plt.show()
# Here we can see the distribution of age parameter with respect to gender and race.

#From the dataframe distribution,we could see that,we got less data for age above 60 , so we can omit it for better model creation.
df = df[(df['age'] < 60)]
df.describe()


# Creating batches of data, which will be utilised to feed both the photos and their labels into the Keras multi-output model 
# (rather than loading the entire dataset into memory at once, which could result in an out of memory error).

p = np.random.permutation(len(df))
train_up_to = int(len(df) * Train_Test_Split)
train_idx = p[:train_up_to]
test_idx = p[train_up_to:]

# spliting train_idx further into training and validation set
train_up_to = int(train_up_to * Train_Test_Split)
train_idx, valid_idx = train_idx[:train_up_to], train_idx[train_up_to:]

# Here we need to OHE gender and race prior feeding it into the model

df['gender_id'] = df['gender'].map(lambda gender: Gender_ID_Map[gender])
df['race_id'] = df['race'].map(lambda race: Race_ID_Map[race])

max_age = df['age'].max()

# Before entering the image into the network, this function is used to do some minimal preprocessing on it.
def preprocess_image(img_path): 
    im = Image.open(img_path)
    im = im.resize((Img_Width, Img_Height))
    im = np.array(im) / 255.0
    return im

# When training/validating/testing our model, we use this function to generate a batch of images.
def data_generator(df, img_indices, for_training, batch_size=16):
    images, ages, races, genders = [], [], [], []
    while True:
        for i in img_indices:
            person = df.iloc[i]
            file, age, race, gender = person['file'], person['age'], person['race_id'], person['gender_id']
            im = preprocess_image(file)
            images.append(im)
            ages.append(age / max_age)
            races.append(to_categorical(race, len(Race_ID_Map)))
            genders.append(to_categorical(gender, 2))
            if len(images) >= batch_size:
                yield np.array(images), [np.array(ages), np.array(races), np.array(genders)]
                images, ages, races, genders = [], [], [], []
        if not for_training:
            break


#Creating CNN model architecture

#Function for creating convolution_block
def convolution_block(inp, filters=32, bn=True, pool=True):
    x = Conv2D(filters=filters, kernel_size=3, activation='relu')(inp)
    if bn:
        x = BatchNormalization()(x)
    if pool:
        x = MaxPool2D()(x)
    return x

#Input Layer
input_layer = Input(shape=(Img_Height, Img_Width, 3))

#Convolution and Pooling
x = convolution_block(input_layer, filters=32, bn=False, pool=False)
x = convolution_block(x, filters=64)
x = convolution_block(x, filters=96)
x = convolution_block(x, filters=128)
x = convolution_block(x, filters=160)
x = convolution_block(x, filters=192)
bottleneck = GlobalMaxPool2D()(x)

#Hidden layer for Age calculation
a = Dense(units=128, activation='relu')(bottleneck)
#Output layer for Age calculation
age_output = Dense(units=1, activation='sigmoid', name='age_output')(a)

#Hidden layer for Race prediction
r = Dense(units=128, activation='relu')(bottleneck)
#Output layer for Race prediction
race_output = Dense(units=len(Race_ID_Map), activation='softmax', name='race_output')(r)

#Hidden layer for Gender prediction
g = Dense(units=128, activation='relu')(bottleneck)
#Output layer for Gender prediction
gender_output = Dense(units=len(Gender_ID_Map), activation='softmax', name='gender_output')(g)

model = Model(inputs=input_layer, outputs=[age_output, race_output, gender_output])
model.compile(optimizer='rmsprop', 
              loss={'age_output': 'mse', 'race_output': 'categorical_crossentropy', 'gender_output': 'categorical_crossentropy'},
              loss_weights={'age_output': 2., 'race_output': 1.5, 'gender_output': 1.},
              metrics={'age_output': 'mae', 'race_output': 'accuracy', 'gender_output': 'accuracy'})
model.summary()


#Traning the model
batch_size = 64
valid_batch_size = 64
train_gen = data_generator(df, train_idx, for_training=True, batch_size=batch_size)
valid_gen = data_generator(df, valid_idx, for_training=True, batch_size=valid_batch_size)

callbacks = [
    ModelCheckpoint("./model_checkpoint", monitor='val_loss')
]

history = model.fit(train_gen,
                    steps_per_epoch=len(train_idx)//batch_size,
                    epochs=10,
                    callbacks=callbacks,
                    validation_data=valid_gen,
                    validation_steps=len(valid_idx)//valid_batch_size)


#Function for plotting the accuracy of the model
def  plot_train_history(history):
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    axes[0].plot(history.history['race_output_accuracy'], label='Race Train accuracy')
    axes[0].plot(history.history['val_race_output_accuracy'], label='Race Val accuracy')
    axes[0].set_xlabel('Epochs')
    axes[0].legend()
    
    axes[1].plot(history.history['gender_output_accuracy'], label='Gender Train accuracy')
    axes[1].plot(history.history['val_gender_output_accuracy'], label='Gener Val accuracy')
    axes[1].set_xlabel('Epochs')
    axes[1].legend()

    axes[2].plot(history.history['age_output_loss'], label='Age Train MAE')
    axes[2].plot(history.history['val_age_output_loss'], label='Age Val MAE')
    axes[2].set_xlabel('Epochs')
    axes[2].legend()  

    axes[3].plot(history.history['loss'], label='Training loss')
    axes[3].plot(history.history['val_loss'], label='Validation loss')
    axes[3].set_xlabel('Epochs')
    axes[3].legend()
    plt.show()

plot_train_history(history)


#Evaluating the model
test_batch_size=128
test_gen = data_generator(df, test_idx, for_training=False, batch_size=test_batch_size)
print(dict(zip(model.metrics_names, model.evaluate_generator(test_gen, steps=len(test_idx)//128))))

test_batch_size=128
test_gen = data_generator(df, test_idx, for_training=False, batch_size=test_batch_size)
x_test, (age_true, race_true, gender_true)= next(test_gen)
age_pred, race_pred, gender_pred = model.predict_on_batch(x_test)


race_true, gender_true = race_true.argmax(axis=-1), gender_true.argmax(axis=-1)
race_pred, gender_pred = race_pred.argmax(axis=-1), gender_pred.argmax(axis=-1)
age_true = age_true * max_age
age_pred = age_pred * max_age

#Generating the Classification report
print("Classification report for race")
print(classification_report(race_true, race_pred))

print("\nClassification report for gender")
print(classification_report(gender_true, gender_pred))


#Generating the Confusion matrix
cf_matrix_race = confusion_matrix(race_true, race_pred)
cf_matrix_gender = confusion_matrix(gender_true, gender_pred)


#Displaying the Confusion matrix by means of Heatmat on gender attribute
ax = sns.heatmap(cf_matrix_gender, annot=True, cmap='Blues')

ax.set_title('Confusion Matrix on Gender Attribute\n\n');
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values ');

# Ticket labels - List must be in alphabetical order
ax.xaxis.set_ticklabels(['Male','Female'])
ax.yaxis.set_ticklabels(['Male','Female'])

## Display the visualization of the Confusion Matrix.
plt.show()


#Displaying the Confusion matrix by means of Heatmat on race attribute
ax = sns.heatmap(cf_matrix_race, annot=True, cmap='Blues')

ax.set_title('Confusion Matrix on Race Attribute\n\n');
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values ');

# Ticket labels - List must be in alphabetical order
ax.xaxis.set_ticklabels(['White','Black','Asian','Indian','Other'])
ax.yaxis.set_ticklabels(['White','Black','Asian','Indian','Other'])


# Display the visualization of the Confusion Matrix.
plt.show()

#Displaying predicted details on the top and actual details on the bottom of the images
n = 16
random_indices = np.random.permutation(n)
n_cols = 4
n_rows = math.ceil(n / n_cols)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 20))
for i, img_idx in enumerate(random_indices):
    ax = axes.flat[i]
    ax.imshow(x_test[img_idx])
    ax.set_title('Age:{}, Sex:{}, Race:{}'.format(int(age_pred[img_idx]), ID_Gender_Map[gender_pred[img_idx]], ID_Race_Map[race_pred[img_idx]]))
    ax.set_xlabel('Age:{}, Sex:{}, Race:{}'.format(int(age_true[img_idx]), ID_Gender_Map[gender_true[img_idx]], ID_Race_Map[race_true[img_idx]]))
    ax.set_xticks([])
    ax.set_yticks([])
plt.show()