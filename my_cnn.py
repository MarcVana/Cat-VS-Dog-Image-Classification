"""
Created on Sun Apr 26 14:33:16 2020

MY !FIRST! CONVOLUTIONAL NEURAL NETWORK

@author: Marc
"""

###############################################################################################
# PART 1 - Building the Convolutional Neural Network

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(64, (3, 3), input_shape=(64, 64, 3), activation='relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full Connection
classifier.add(Dense(units = 256, activation = 'relu'))
classifier.add(Dropout(0.2))
classifier.add(Dense(units = 1, activation = 'sigmoid'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

###############################################################################################
# PART 2 - Fitting the Convolutional Neural Network to the images
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale = 1. / 255,
        zca_whitening = True,
        rotation_range = 15,
        shear_range = 0.2,
        zoom_range = 0.2,
        channel_shift_range = 0.2,
        vertical_flip = True,
        horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1. / 255)

training_set = train_datagen.flow_from_directory('dataset/training_set',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

history = classifier.fit_generator(training_set,
                         steps_per_epoch = 719,
                         epochs = 50,
                         validation_data = test_set,
                         validation_steps = 2000)

# Plotting the training and testing history
import matplotlib.pyplot as plt
import numpy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('50 epochs')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plt.savefig('50_epochs_32b_moredata_bigNN_dropout.png')

# Save model
import joblib
filename = 'cnn_data.sav'
joblib.dump(classifier, filename)

# Import the model
loaded_model = joblib.load(filename)
classifier = loaded_model

import numpy as np
from keras.preprocessing import image
test_image = image.load_img('dataset/single_prediction/cat_or_dog_2.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
#training_set.class_indices
if result[0][0] == 0.0:
    prediction = 'cat'
else:
    prediction = 'dog'

print(prediction)