import numpy as np


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
            data[index].append(float(item))
        line = f.readline()
        data[index][7] = int(data[index][7])
        index += 1
    f.close()
    # data = np.array(data)
    return data


def print_data(data):
    for item in data:
        print(item)


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

    np.random.shuffle(output_1)
    training_data_output_1 = output_1[:int(len(output_1) * ratio)]
    test_data_output_1 = output_1[int(len(output_1) * ratio):]

    np.random.shuffle(output_2)
    training_data_output_2 = output_2[:int(len(output_2) * ratio)]
    test_data_output_2 = output_2[int(len(output_2) * ratio):]

    np.random.shuffle(output_3)
    training_data_output_3 = output_3[:int(len(output_3) * ratio)]
    test_data_output_3 = output_3[int(len(output_3) * ratio):]

    training = training_data_output_1 + training_data_output_2 + training_data_output_3
    test = test_data_output_1 + test_data_output_2 + test_data_output_3
    np.random.shuffle(training)
    np.random.shuffle(test)

    return training, test


# a function that calculates the output of the node (based on its inputs and the weights on individual inputs)
# This is important as it makes understanding how relevant is every value from a vector.
def softmax(x):
    # transform list to numpy array
    v = np.array(x)
    # cut the last column of the copy with the expected output
    v = v[:, :-1]
    s = np.max(v, axis=1, keepdims=True)
    e_x = np.exp(v - s)
    div = np.sum(e_x, axis=1, keepdims=True)
    return e_x / div


# for the gradient descent we need the derivative of the softmax function
def softmax_derivative(x):
    s = softmax(x)
    # Reshape the softmax vector to a column vector
    s = s.reshape(-1, 1)

    # Compute the Jacobian matrix
    jacobian_matrix = np.diagflat(s) - np.dot(s, s.T)

    return jacobian_matrix


def initialize_params(input_layer, hidden_neurons_per_layer):
    # how powerful is a connection between the input layer and the hidden layer
    weights = []
    # the constant which is added to the product of features and weights.
    bias = []
    # xavier initialization
    for i in range(nr_hidden_layers):
        if i == 0:
            weights.append(np.random.randn(input_layer, hidden_neurons_per_layer) * np.sqrt(1 / input_layer))
            bias.append(np.random.randn(hidden_neurons_per_layer) * np.sqrt(1 / input_layer))
        else:
            weights.append(np.random.randn(hidden_neurons_per_layer, hidden_neurons_per_layer) * np.sqrt(
                1 / hidden_neurons_per_layer))
            bias.append(np.random.randn(hidden_neurons_per_layer) * np.sqrt(1 / hidden_neurons_per_layer))

    return weights, bias


def cross_entropy(weights, bias, training_data):
    pass


def forward_propagation(instance, weights, activation_func):
    values = [instance.copy()]
    for x in weights:
        values.append(np.matmul(values[-1], x))
        for index, i in enumerate(values[-1]):
            values[-1][index] = activation_func(i)
    return values


data = extract_data("seeds_dataset.txt")
training_data, test_data = split_data(data, 0.8)
nr_input_layer = 7  # 7 atribute de intrare
nr_output_layer = 3  # 3 clase
nr_hidden_layers = 2
nr_hidden_neurons_per_layer = int((2 / 3) * nr_input_layer + nr_output_layer)
learning_rate = 0.1
max_epochs = 1000
weights, bias = initialize_params(nr_input_layer, nr_hidden_neurons_per_layer)

print(cross_entropy(weights, bias, training_data))
