import sqlite3
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Preprocess the data
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Create a SQLite database and save the preprocessing steps and model
conn = sqlite3.connect('iris.db')
cursor = conn.cursor()

# Create table to store preprocessing steps
cursor.execute('''
    CREATE TABLE IF NOT EXISTS preprocessing_steps (
        name TEXT PRIMARY KEY,
        data BLOB
    )
''')

# Save the scaler object
scaler_data = sqlite3.Binary(pickle.dumps(scaler))
cursor.execute("INSERT INTO preprocessing_steps (name, data) VALUES (?, ?)", ('scaler', scaler_data))

# Save the model object
model_data = sqlite3.Binary(pickle.dumps(model))
cursor.execute("INSERT INTO preprocessing_steps (name, data) VALUES (?, ?)", ('model', model_data))

conn.commit()
conn.close()
