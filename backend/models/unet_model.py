# backend/models/unet_model.py
import tensorflow as tf
from tensorflow.keras import layers, models

def build_unet(input_shape=(128,128,3), num_classes=1):
    inputs = layers.Input(shape=input_shape)
    # Downsampling path
    c1 = layers.Conv2D(16, 3, activation='relu', padding='same')(inputs)
    p1 = layers.MaxPooling2D(2)(c1)
    c2 = layers.Conv2D(32, 3, activation='relu', padding='same')(p1)
    p2 = layers.MaxPooling2D(2)(c2)
    c3 = layers.Conv2D(64, 3, activation='relu', padding='same')(p2)
    # Bottleneck
    # Upsampling path
    u2 = layers.Conv2DTranspose(32, 2, strides=2, activation='relu', padding='same')(c3)
    m2 = layers.Concatenate()([u2, c2])
    c4 = layers.Conv2D(32, 3, activation='relu', padding='same')(m2)
    u3 = layers.Conv2DTranspose(16, 2, strides=2, activation='relu', padding='same')(c4)
    m3 = layers.Concatenate()([u3, c1])
    c5 = layers.Conv2D(16, 3, activation='relu', padding='same')(m3)
    outputs = layers.Conv2D(num_classes, 1, activation='sigmoid')(c5)

    model = models.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    # Example: build and summarize model
    model = build_unet()
    model.summary()
    # (In practice, train on labeled data and save weights:)
    # X, y = ...  # load training data
    # model.fit(X, y, epochs=10, batch_size=4)
    # model.save('unet_model.h5')
