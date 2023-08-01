from flask import Flask, render_template, request
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd

app = Flask(__name__)

try:
    with open('fish_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    raise FileNotFoundError("Trained model not found. Please run the Jupyter Notebook to train the model.")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input values from the form
    species = request.form['species']
    length1 = float(request.form['length1'])
    length2 = float(request.form['length2'])
    length3 = float(request.form['length3'])
    height = float(request.form['height'])
    width = float(request.form['width'])

    input_data = pd.DataFrame([[species, length1, length2, length3, height, width]],
                              columns=['Species', 'Length1', 'Length2', 'Length3', 'Height', 'Width'])

    le = LabelEncoder()
    input_data['Species'] = le.fit_transform(input_data['Species'])

   
    prediction = model.predict(input_data)[0]

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
