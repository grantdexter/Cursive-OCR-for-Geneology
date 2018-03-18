"""
The goal of this file is to establish smaller classification methods which can be used as inputs to a more intelligent model

Attempt to segment letters into general categories to help with classification
Use attributes like:
    Contains tall letters or no
    Contains numbers
    Is single letter or multiple letters
    Has space or no (two word parts or all one)
    Has Capital letter or no

"""
import numpy as np
import random
import os
from keras.preprocessing.image import ImageDataGenerator

import load_images_dataset
import custom_models

path = os.getcwd() + "/dataset"



# n_classes = 2
base_layers = 3
epochs = 20
batch_size = 1
conv_size = 4
pool_size = 2


imgs, labels, name_labels, n_classes, input_shape = \
        load_images_dataset.read_my_csv("has_tall_letters_undersampled.txt", \
        input_shape=(60, 70, 3), channels=3, one_hot=False)


    def augment_data():
        train_datagen = ImageDataGenerator(
                rescale=1./255,
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True,)

        # Note that the validation data should not be augmented!
        test_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory(
                train_dir='C:\Users\grant\Repos\Cursive-OCR-for-Geneology\all_dataset_combined',
                target_size=(60, 70),
                batch_size=32,
                class_mode='binary')

        validation_generator = test_datagen.flow_from_directory(
                validation_dir='C:\Users\grant\Repos\Cursive-OCR-for-Geneology\all_dataset_combined',
                target_size=(60, 70),
                batch_size=32,
                class_mode='binary')

        # early_stop = EarlyStopping(monitor='val_loss', patience=6, verbose=1)
        history_aug = model_aug.fit_generator(train_generator, steps_per_epoch=100, epochs=60,
                                              validation_data=validation_generator, validation_steps=50, verbose=0)

n_test, n, x_test, x_train, y_test, y_train = load_images_dataset.divide_data(imgs, labels, name_labels)

# print(x_train[:5])

for x in range(1, 10):
    print(labels[x], name_labels[x])

model = custom_models.basic_cnn('relu', 'mean_squared_error', \
                                x_train, y_train, input_shape, n_classes, \
                                epochs=epochs, batch_size=batch_size)

score = model.evaluate(x_test, y_test, verbose=1)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
print(score)

pred = model.predict(x_test)

print("predictions finished")

for i in range (0, len(x_test)):
    actuals = ""
    # for label in y[n+i]:
    for index in np.where(labels[n+i]==1)[0]:
        # actuals += " {}".format(label_dict["idx2word"][index])
        actuals += str(index+1)
    print("---------------------------------------\nActual: {}".format(actuals))

    # label_dict["idx2word"][s],y[n+i][s]) for s in y[n+i])
    # print("Prediction: {}".format(pred[i]))

    preds = pred[i]
    formatted_preds = []
    for ind, val in enumerate(preds):
        # print(ind)
        # print(val)
        formatted_preds.append("{} probability of label: {}".format(val, ind+1))
    formatted_preds.sort()
    for x in formatted_preds:
        print(x)
    # print("Predicted: {}".format(formatted_preds.sort()))
    # for i2 in range (0, len(label_dict["idx2word"])):
        # if pred[i][i2] > 0.2:
        # print("\"{}\":{}".format(label_dict["idx2word"][i2], pred[i][i2]))
    print("--------------------------------------")
