import os
import zipfile

#只运行一次->
# local_zip = '/Users/vst/PycharmProjects/ML-1/TestData/rps.zip'
# zip_ref = zipfile.ZipFile(local_zip, 'r')
# zip_ref.extractall('/Users/vst/PycharmProjects/ML-1/TestData/')
# zip_ref.close()
#
# local_zip = '/Users/vst/PycharmProjects/ML-1/TestData/rps-test-set.zip'
# zip_ref = zipfile.ZipFile(local_zip, 'r')
# zip_ref.extractall('/Users/vst/PycharmProjects/ML-1/TestData/')
# zip_ref.close()
#<-只运行一次
# /Users/vst/PycharmProjects/ML-1/TestData

rock_dir = os.path.join('/Users/vst/PycharmProjects/ML-1/TestData/rps/rock')
paper_dir = os.path.join('/Users/vst/PycharmProjects/ML-1/TestData/rps/paper')
scissors_dir = os.path.join('/Users/vst/PycharmProjects/ML-1/TestData/rps/scissors')

print('total training rock images:', len(os.listdir(rock_dir)))
print('total training paper images:', len(os.listdir(paper_dir)))
print('total training scissors images:', len(os.listdir(scissors_dir)))

rock_files = os.listdir(rock_dir)
print(rock_files[:10])

paper_files = os.listdir(paper_dir)
print(paper_files[:10])

scissors_files = os.listdir(scissors_dir)
print(scissors_files[:10])

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pic_index = 2

next_rock = [os.path.join(rock_dir, fname)
             for fname in rock_files[pic_index - 2:pic_index]]
next_paper = [os.path.join(paper_dir, fname)
              for fname in paper_files[pic_index - 2:pic_index]]
next_scissors = [os.path.join(scissors_dir, fname)
                 for fname in scissors_files[pic_index - 2:pic_index]]

for i, img_path in enumerate(next_rock + next_paper + next_scissors):
    # print(img_path)
    img = mpimg.imread(img_path)
    plt.imshow(img)
    plt.axis('Off')
    plt.show()

#Constructing DNN by tf

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import keras_preprocessing
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

TRAINING_DIR = "/Users/vst/PycharmProjects/ML-1/TestData/rps/"
training_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

VALIDATION_DIR = "/Users/vst/PycharmProjects/ML-1/TestData/rps-test-set/"
validation_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = training_datagen.flow_from_directory(
    TRAINING_DIR,
    target_size=(150, 150),
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=(150, 150),
    class_mode='categorical'
)

model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image 150x150 with 3 bytes color
    # This is the first convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The third convolution
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The fourth convolution
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

history = model.fit_generator(train_generator, epochs=25, validation_data=validation_generator, verbose=1)

model.save("rps.h5")#Save the training data in .h5 file.

#Analyze the result.

import matplotlib.pyplot as plt
from keras.models import load_model
model = load_model("/Users/vst/PycharmProjects/rps.h5")
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.figure()


plt.show()

