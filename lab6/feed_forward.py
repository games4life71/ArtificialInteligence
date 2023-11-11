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
    return data


def print_data(data):
    for item in data:
        print(item)


def split_data(data, ratio):
    output_1= []
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


def softmax(x):
    # transform list to numpy array
    x = np.array(x)
    # cut the last column with the expected output
    x = x[:, :-1]
    s = np.max(x, axis=1)
    s = s[:, np.newaxis]  # necessary step to do broadcasting
    e_x = np.exp(x - s)
    div = np.sum(e_x, axis=1)
    div = div[:, np.newaxis]  # dito
    return e_x / div


def initialize_params():
    nr_input_layer = 7   # 7 atribute de
    nr_output_layer = softmax(training_data)
    nr_output_neurons_per_layer = 3  # 3 clase
    alpha = 2
    nr_hidden_layers = (len(training_data)-1) / (alpha * (nr_input_layer + nr_output_layer))
    nr_hidden_neurons_per_layer = (2//3)*nr_input_layer + nr_output_layer
    learning_rate = 0.1
    max_epochs = 1000
    weights_input_hidden = 0


data = extract_data("seeds_dataset.txt")
training_data, test_data = split_data(data, 0.8)

