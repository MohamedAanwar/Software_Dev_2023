import os
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Rescaling
from keras.applications import VGG16
from keras.models import Model
import pandas as pd
import shutil

class CNNModel:
    def __init__(self, input_shape, num_classes,model):
        self.input_shape = input_shape
        self.num_classes = num_classes
        if model=='vgg16':
           self.model = self.VGG16Model()
        else:
            self.model = self.build_model()

    def build_model(self):
        try:
            model = Sequential()
            model.add(Rescaling(1.0 / 255.0, input_shape=self.input_shape))
            model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=self.input_shape))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dense(self.num_classes, activation='softmax'))
            return model
        except Exception as ex:
            print(ex)
            return ex
        


    def VGG16Model(self):
        try:
            base_model = VGG16(weights='imagenet',
                            include_top=False, input_shape=self.input_shape)
            x = Flatten()(base_model.output)
            x = Dense(128, activation='relu')(x)
            output = Dense(self.num_classes, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=output)

            # Freeze the layers of the pre-trained model
            for layer in base_model.layers:
                layer.trainable = False

            return model
        except Exception as ex:
            print(ex)
            return ex

    def compile_model(self):
        try:
            self.model.compile(loss='categorical_crossentropy',
                            optimizer='adam',
                            metrics=['accuracy'])
        except Exception as ex:
            print(ex)
            return ex

    def train_model(self, train_dir, batch_size, epochs):
        try:
            train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)
            train_generator = train_datagen.flow_from_directory(directory=train_dir,
                                                                target_size=self.input_shape[:2],
                                                                batch_size=batch_size,
                                                                class_mode='categorical',
                                                                shuffle=True)

            self.model.fit(train_generator,
                        steps_per_epoch=train_generator.samples // batch_size,
                        epochs=epochs
                        )  
        except Exception as ex:
            print(ex)
            return ex
        
    def prepareClasses(self, image_folder):
        try:
           # Create a dictionary to store image names and their corresponding directories
            image_directories = {}

            # Iterate over the images in the folder
            for filename in os.listdir(image_folder):
                if os.path.isfile(os.path.join(image_folder, filename)):
                    # Extract the image name without the file extension
                    image_name = os.path.splitext(filename)[0][4:]
                    
                    # Create the directory if it doesn't exist
                    if image_name not in image_directories:
                        image_directories[image_name] = os.path.join(image_folder, image_name)
                        os.makedirs(image_directories[image_name], exist_ok=True)
                    
                    # Move the image to its corresponding directory
                    shutil.move(os.path.join(image_folder, filename), image_directories[image_name])

        except Exception as ex:
            print(ex)
            return ex



    def save_model(self, model_path):
        try:
            self.model.save(model_path)
        except Exception as ex:
            print(ex)
            return ex

    def load_model(self, model_path):
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as ex:
            print(ex)
            return ex

    def predict(self, image_path):
        try:
            image = tf.keras.preprocessing.image.load_img(image_path, target_size=self.input_shape[:2])
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = image / 255.0
            prediction = self.model.predict(image)
            class_index = np.argmax(prediction)
            return class_index
        except Exception as ex:
           print(ex)
           return ex


if __name__=='__main__':
   
    # Example usage:
    input_shape = (256, 256, 3)  # Input image shape (height, width, channels)
    train_dir = 'D:/Frame/acute crow 3 rd black novel place TA 16 h named'
    num_classes = sum([1 for item in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, item))]) # used to count number of dirs i trianing dir (number of class)
    model = CNNModel(input_shape, num_classes,'vgg16')
    model.compile_model()
    
    batch_size = 32
    epochs = 60
    model.train_model(train_dir,batch_size,epochs)


    
    model_path = 'D:\Frame' # Path to save the trained model
    model.save_model(model_path)





    '''
    Note

    folder structure for training data should be like:

    trainDir/
        class A/
            1.png
            2.png

        class B/
            1.png
            2.png

        class C/
            1.png
            2.png

            
    and so on
    sub dirs on training dir are class names
    '''