# -*- coding: utf-8 -*-
"""Preprocessing data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SzV7nH-BEKqbPiAJXR-xgiGtcHxBWVuQ

## Preprocessing data (normalization and standardization)
In terms of scaling values, neural networks tend to prefer normalization.

If not sure you could try both to see which one performs better.
"""

# Import required libraries
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read in the insuarance dataset
insuarance = pd.read_csv('https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv')
insuarance

"""To prepare our data, we can borrow a few classes from scikit-learn"""

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder
from sklearn.model_selection import train_test_split

# Create a column transformer
ct = make_column_transformer(
    (MinMaxScaler(),['age','bmi','children']),# turn all these values in the columns to between 0 and 1
    (OneHotEncoder(handle_unknown='ignore'),['sex','smoker','region'])
)

# Create X and y
X = insuarance.drop('charges', axis = 1)
y = insuarance['charges']

# Build our train and test sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Fit the column transformer to our training data
ct.fit(X_test)

# Transform trainig and test data with normalization (MinMaxScaler) and HotOneEncoder
X_train_normal = ct.transform(X_train)
X_test_normal = ct.transform(X_test)

# What the data looks like
X_train_normal[0]

"""The data has now been normalized and one_hot_encoded now we can an use it to build our model"""

tf.random.set_seed(42)

# Build the model
insuarance_model_4 = tf.keras.Sequential([
    tf.keras.layers.Dense(100),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Dense(1)
])

# Compile the model
insuarance_model_4.compile(
    loss = tf.keras.losses.mae,
    optimizer = tf.keras.optimizers.Adam(),
    metrics=['mae']
)

# Fit the model
insuarance_model_4.fit(X_train_normal,y_train,epochs=200)

# evaluate the model
insuarance_model_4.evaluate(X_test_normal,y_test)