from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('model1.pkl', 'rb') as file:
    model = pickle.load(file)


# Read the dataset
df = pd.read_csv("Filtered_Salary_data.csv")

# Home route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict')
def form():
    return render_template('predict.html')

@app.route('/insights')
def index():
    return render_template('insights.html')


# Prediction route
@app.route('/predict', methods=['POST'])


def predict():
    # Get the input values from the form
    gre_score = int(request.form['GRE Score'])
    toefl_score = int(request.form['TOEFL Score'])
    university_rating = int(request.form['University Rating'])
    sop = float(request.form['SOP'])
    lor = float(request.form['LOR'])
    cgpa = float(request.form['CGPA'])
    research = int(request.form['Research'])
    branch = request.form['Branch']

    # Make prediction using the loaded model
    prediction = model.predict(np.array([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]]))

    # logic wala game
    if branch == 'CS':
        prediction -= 0.4
    if branch == 'ENTC':
        prediction -= 0.22
    if branch == 'Mech':
        prediction -= 0.12
    if branch == 'Civil':
        prediction += 0.05

    if university_rating == 1:
        prediction -= 0.12
    if university_rating == 2:
        prediction -= 0.05
    if university_rating == 4:
        prediction += 0.05
    if university_rating == 5:
        prediction += 0.1

    if(prediction>1):
        prediction = prediction - (prediction-1)

    # Return the predicted chance of admission
    return render_template('result.html', prediction=prediction[0])


# insights model 

@app.route('/data')
def get_data():
    job_title = request.args.get('jobTitle')
    filtered_df = df[df['Job Title'] == job_title]
    data = {
        'years_experience': filtered_df['Years of Experience'].tolist(),
        'salary': filtered_df['Salary'].tolist()
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
