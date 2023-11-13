import copy

import numpy as np


# extract data from file
def extract_data(file_name):
    f = open(file_name, "r")
    data = []
    line = f.readline()
    index = 0
    while line:
        line = line.strip("\n")
        line = line.split()
        data.append([])
        for item in line:
            data[index].append(float(item))  # convert the input to float
        line = f.readline()
        data[index][7] = int(data[index][7])  # convert the output to int
        index += 1
    f.close()
    # data = np.array(data)
    return data


def print_data(data):
    for item in data:
        print(item)


# split the data into training and test data
def split_data(data, ratio):
    output_1 = []
    output_2 = []
    output_3 = []
    for item in data:
        if item[7] == 1:
            output_1.append(item)
        elif item[7] == 2:
            output_2.append(item)
        else:
            output_3.append(item)

    # np.random.shuffle(output_1)

    training_data_output_1 = output_1[:int(len(output_1) * ratio)]
    test_data_output_1 = output_1[int(len(output_1) * ratio):]

    # np.random.shuffle(output_2)
    training_data_output_2 = output_2[:int(len(output_2) * ratio)]
    test_data_output_2 = output_2[int(len(output_2) * ratio):]

    # np.random.shuffle(output_3)
    training_data_output_3 = output_3[:int(len(output_3) * ratio)]
    test_data_output_3 = output_3[int(len(output_3) * ratio):]

    training = training_data_output_1 + training_data_output_2 + training_data_output_3
    test = test_data_output_1 + test_data_output_2 + test_data_output_3
    np.random.shuffle(training)
    np.random.shuffle(test)

    return training, test


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def softmax(x):
    e_x = np.exp(x - np.max(x))  # subtract max(x) for numerical stability
    return e_x / e_x.sum(axis=0)


# for the gradient descent we need the derivative of the softmax function
def softmax_derivative(x):
    s = softmax(x)
    # Reshape the softmax vector to a column vector
    s = s.reshape(-1, 1)

    # Compute the Jacobian matrix
    jacobian_matrix = np.diagflat(s) - np.dot(s, s.T)

    return jacobian_matrix


# for each neuron from the hidden layer, we have a vector of weights and a bias
def initialize_params(input_layer, hidden_neurons_per_layer):
    # how powerful is a connection between the input layer and the hidden layer
    weights = []
    np.random.seed(1)
    # the constant which is added to the product of features and weights.
    bias = []
    # xavier initialization
    for i in range(nr_hidden_layers):
        if i == 0:
            # if it is the first hidden layer, the input is the number of features

            weights.append(np.random.randn(input_layer, hidden_neurons_per_layer) * np.sqrt(1 / input_layer))
            bias.append(np.random.randn(hidden_neurons_per_layer) * np.sqrt(1 / input_layer))
        else:
            # if it is not the first hidden layer, the input is the number of neurons from the previous layer
            weights.append(np.random.randn(hidden_neurons_per_layer,
                                           hidden_neurons_per_layer)
                           * np.sqrt(1 / hidden_neurons_per_layer))

            bias.append(np.random.randn(hidden_neurons_per_layer) * np.sqrt(1 / hidden_neurons_per_layer))

    # initialize the weights and the bias for the output layer
    weights.append(np.random.randn(hidden_neurons_per_layer, nr_output_layer) * np.sqrt(1 / hidden_neurons_per_layer))
    bias.append(np.random.randn(nr_output_layer) * np.sqrt(1 / hidden_neurons_per_layer))

    return weights, bias


# cross entropy compares the predicted output with the actual output
def cross_entropy(output_layer, desired_output):
    output_layer = output_layer.reshape(-1, 1)
    desired_output = desired_output.reshape(-1, 1)
    return -np.sum(desired_output * np.log(output_layer))


def forward_propagation(instance, weights, biases, activation_func):
    caches = []
    A = instance.copy()

    L = len(weights) - 1  # number of layers in the neural network
    for l in range(1, L):
        A_prev = A  # this is the input for the current layer,which is the activation of the previous layer
        A, cache = linear_activation_forward(A_prev, weights[l], activation_func, biases[l], False)
        caches.append(cache)

    # this is the last layer

    AL, cache = linear_activation_forward(A, weights[L], softmax, biases[L], True)
    caches.append(cache)
    return AL, caches


def linear_activation_forward(A_prev, W, activation_func, b, is_last_layer):
    if is_last_layer:
        # reshape the output
        print("A_prev got heree")
        # sleep

        # A_prev = A_prev.reshape(-1, 1)

    Z, linear_cache = linear_forward(A_prev, W, b)
    A = activation_func(Z)
    cache = linear_cache

    return A, cache


def linear_forward(A_prev, W, b):
    A_prev = np.array(A_prev, copy=True)
    Z = np.dot(A_prev, W)
    # this computes the linear part of the neuron (the sum of the products of the weights and the
    # inputs)
    cache = (A_prev, W, b)  # this is the cache that will be used in the backpropagation
    return Z, cache


data = extract_data("seeds_dataset.txt")
training_data, test_data = split_data(data, 0.8)

nr_input_layer = 7  # 7 atribute de intrare (fara output)
nr_output_layer = 3  # 3 clase de output
nr_hidden_layers = 2  # 2 hidden layers

# each neuron from a hidden layer has as input all the neurons from the previous layer
# and as output all the neurons from the next layer

nr_hidden_neurons_per_layer = int((2 / 3) * nr_input_layer + nr_output_layer)  # 9 neurons per hidden layer

learning_rate = 0.1
max_epochs = 1000

# initialize the weights and the bias for each neuron from the hidden layer
weights, bias = initialize_params(nr_input_layer, nr_hidden_neurons_per_layer)


def modify_training_data(training_data):
    # remove the last column from the training data
    training_data_copy = copy.deepcopy(training_data)
    for item in training_data_copy:
        item.pop()
    return training_data_copy


training_data_modified = modify_training_data(training_data)
# print(training_data[0])

AL, caches = forward_propagation(training_data_modified[0], weights, bias, sigmoid)
print(AL)
# compute the error
#
# error = cross_entropy(AL, training_data[0][6])
# print(error)

real_distribution = {1: [1, 0, 0], 2: [0, 1, 0], 3: [0, 0, 1]}

error = cross_entropy(AL, np.array(real_distribution[training_data[0][7]]))

print("error: ", error)
