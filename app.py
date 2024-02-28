from flask import Flask, render_template, request
import pickle
import numpy as np
import pygame

app = Flask(__name__)

# Load the trained model
with open('model1.pkl', 'rb') as file:
    model = pickle.load(file)

# Initialize Pygame mixer
pygame.mixer.init()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

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

    # Play music if prediction exceeds 0.78
    if prediction > 0.8:
        pygame.mixer.music.load('/Users/kartikeysapkal/Downloads/TpVxP9AC-Chipi-Chipi-Chapa-Chapa-Original-Song.mp3')
        pygame.mixer.music.play(-1)

    if prediction < 0.8:
        pygame.mixer.music.load('/Users/kartikeysapkal/Downloads/tf_nemesis.mp3')
        pygame.mixer.music.play(-1)


    # Return the predicted chance of admission
    return render_template('result.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
