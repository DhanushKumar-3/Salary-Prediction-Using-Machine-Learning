from flask import Flask, render_template, request
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__)

# Load model & encoder
model = pickle.load(open("model/salary_model.pkl", "rb"))
encoder = pickle.load(open("model/encoder.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    experience = request.form.get('experience')
    job_role = request.form.get('job_role')
    location = request.form.get('location')

    df = pd.DataFrame([[experience, job_role, location]],
                      columns=['experience', 'job_role', 'location'])

    encoded = encoder.transform(df).toarray()
    prediction = model.predict(encoded)[0]
    prediction = max(prediction, 0)   # avoid negative salary

    return render_template("result.html", salary=round(prediction, 2))

if __name__ == "__main__":
    app.run(debug=True)