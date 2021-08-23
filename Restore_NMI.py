import matplotlib
matplotlib.use('TkAgg')

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import matplotlib.pyplot as plt
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

# Reading the Dataset
def read_dataset():
    df = pd.read_csv("sonar.all-data.csv")
    #print len("Length = ",df.columns)
    X = df[df.columns[0:60]].values
    y = df[df.columns[60]]

    #Encode the dependent variable
    encoder = LabelEncoder()
    encoder.fit(y)
    y = encoder.transform(y)
    Y = one_hot_encode(y)
    print("X,shape ", X.shape)
    return (X,Y)

# Define the encoder function
def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_lables = len(np.unique(labels))
    one_hot_encode  = np.zeros((n_labels, n_unique_lables))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode

# Read the dataset
X, Y = read_dataset()

# Shuffle the dataset to mix up the rows
X, Y = shuffle(X, Y, random_state = 1)

# Convert the dataset into train and test part
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.20, random_state=415)

# Inspect the shape of the training and testing
print(train_x.shape)
print(train_y.shape)
print(test_x.shape)

##############
## Restore NMI - Change 1
model_path = "C:/Users/Sarbani chatterjee/PycharmProjects/Sonar_Detection_Mechanism/MyModel"
#C:\Users\Sarbani chatterjee\PycharmProjects\Sonar_Detection_Mechanism\MyModel

# Define the important parameters and variable to work with the tensors
learning_rate = 0.3
training_epochs = 1000
cost_history = np.empty(shape=[1], dtype = float)
n_dim = X.shape[1]
print("n_dim", n_dim)
n_class = 2

# Define the number of hidden layers and the numbers of neurons for each layer
n_hidden_1 = 60
n_hidden_2 = 60
n_hidden_3 = 60
n_hidden_4 = 60

x = tf.compat.v1.placeholder(tf.float32, [None, n_dim])
W = tf.Variable(tf.zeros([n_dim, n_class]))
b = tf.Variable(tf.zeros([n_class]))
y_ = tf.compat.v1.placeholder(tf.float32, [None, n_class])


#Define the model
def multilayer_perceptron(x, weights, biases):
    #Hidden layer with RELU activationsd
    layer_1 = tf.add(tf.matmul(x,weights['h1']), biases['b1'])
    layer_1 = tf.nn.sigmoid(layer_1)

    layer_2 = tf.add(tf.matmul(layer_1,weights['h2']), biases['b2'])
    layer_2 = tf.nn.sigmoid(layer_2)

    layer_3 = tf.add(tf.matmul(layer_2,weights['h3']), biases['b3'])
    layer_3 = tf.nn.sigmoid(layer_2)

    layer_4 = tf.add(tf.matmul(layer_3,weights['h4']), biases['b4'])
    layer_4 = tf.nn.relu(layer_2)

    out_layer = tf.add(tf.matmul(layer_4, weights['out']), biases['out'])
    return out_layer


# Define the weights and biases fo each layer

weights = {
    'h1': tf.Variable(tf.compat.v1.truncated_normal([n_dim,       n_hidden_1])),
    'h2': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_1,  n_hidden_2])),
    'h3': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_2,  n_hidden_3])),
    'h4': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_3,  n_hidden_4])),
    'out': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_4, n_class]))
}

biases = {
    'b1': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_1])),
    'b2': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_2])),
    'b3': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_3])),
    'b4': tf.Variable(tf.compat.v1.truncated_normal([n_hidden_4])),
    'out': tf.Variable(tf.compat.v1.truncated_normal([n_class]))
}

# Initialize all the variables

init = tf.compat.v1.global_variables_initializer()

############
## Restore NMI - Change 2
saver = tf.compat.v1.train.Saver()

# Call your model defined
y = multilayer_perceptron(x, weights, biases)

# Define the cost function and optimizer
cost_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))
training_step = tf.compat.v1.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

sess = tf.compat.v1.Session()
sess.run(init)
saver.restore(sess, model_path)

prediction = tf.argmax(y,1)
correct_prediction = tf.equal(prediction, tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print("Test Accuracy: ", (sess.run(accuracy, feed_dict={x: test_x, y_: test_y})) )

# Print the final mean square error

print ('******** 0=M=Mine, 1=R=Rock ***********')

for i in range (93,101):
    prediction_run = sess.run(prediction, feed_dict={x:X[i].reshape(1,60)})
    accuracy_run = sess.run(accuracy, feed_dict={x:X[i].reshape(1,60), y_:Y[i].reshape(1,2)})
    print(i,"Original Class: ", int(sess.run(y_[i][1],feed_dict={y_:Y})), " Predicted Values: ", prediction_run[0] )
    print("Accuracy: ",str(accuracy_run*100)+"%")


