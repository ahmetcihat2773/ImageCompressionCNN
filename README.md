# ImageCompressionCNN

## Overview

This project aims to design a classifier that can classify images based on their compression types. Source images are TIFF images, and different datasets are created with various compression types such as JPEG, JPEG 2000, JPEG XR, and BPG. By varying the compression ratio and SSIM values, we aim to increase the diversity of image characteristics and develop a robust classifier.

## Contents

### 1. Image Compression
The `ImageCompression.py` script implements various image compression techniques using libraries such as OpenCV and NumPy. This script includes:
- **Image Resizing:** Using interpolation methods for efficient image resizing.
- **Color Space Transformation:** Converting images to different color spaces to exploit redundancies.
- **Quantization:** Reducing the number of colors to compress image data.
- **Compression Methods:** Applying JPEG, JPEG 2000, JPEG XR, and BPG compression techniques with different ratios and SSIM values.

### 2. Main Script
The `main.py` script serves as the main entry point, integrating image compression and machine learning model training functionalities. It ensures a streamlined workflow for users by:
- **Loading Images and Datasets:** Reading source TIFF images and applying various compression techniques.
- **Preparing Data:** Normalizing and organizing data for training.
- **Invoking Model Training:** Running the training process to build the classifier.

### 3. Model Training
The `train_model.ipynb` notebook contains detailed steps for training machine learning models using TensorFlow/Keras. It covers:
- **Data Preprocessing:** Techniques such as normalization and augmentation to improve model robustness.
- **Model Building:** Constructing a neural network with appropriate architecture.
- **Training the Model:** Defining the training loop with hyperparameter tuning, early stopping, and learning rate scheduling.
- **Model Evaluation:** Assessing performance using metrics like accuracy and loss.
- **Saving and Loading Models:** Demonstrating how to save and reload the trained model.

