import tensorflow as tf
import pandas as pd
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense

df = pd.read_csv('seeds_dataset.txt', sep='\\s+', header=None)

# Assuming df is your DataFrame and the last column is the target
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Encode class values as integers
encoder = LabelEncoder()
encoder.fit(y)
encoded_Y = encoder.transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, encoded_Y, test_size=0.2, random_state=42)

# Define the model
model = Sequential()
model.add(Dense(8, input_dim=X.shape[1], activation='relu'))
model.add(Dense(8, input_dim=X.shape[1], activation='relu'))
model.add(Dense(8, input_dim=X.shape[1], activation='relu'))
model.add(Dense(3, activation='softmax'))  # 3 classes

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, epochs=100, batch_size=3, verbose=1)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Accuracy: {accuracy*100:.2f}%')

# Make a prediction
new_data = pd.read_csv('new_data.txt', sep='\\s+', header=None)

# Preprocess new_data the same way as the training data
X_new = new_data.iloc[:, :-1].values

# Use the model to make predictions
predictions = model.predict_step(X_new)



# Print the predictions
print(predictions)

for prediction in predictions:
    print(prediction*100)