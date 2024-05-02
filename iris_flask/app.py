import sqlite3
import pickle
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load the preprocessing steps and model from the SQLite database
conn = sqlite3.connect('iris.db')
cursor = conn.cursor()

# Load the scaler object
cursor.execute("SELECT data FROM preprocessing_steps WHERE name='scaler'")
scaler_data = cursor.fetchone()[0]
scaler = pickle.loads(scaler_data)

# Load the model object
cursor.execute("SELECT data FROM preprocessing_steps WHERE name='model'")
model_data = cursor.fetchone()[0]
model = pickle.loads(model_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    if data is None:
        return jsonify({'error': 'No data received'}), 400
    try:
        new_data = scaler.transform([[data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']]])
        prediction = model.predict(new_data)
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
