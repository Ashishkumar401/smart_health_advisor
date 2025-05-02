from flask import Flask, render_template, request
from ml_model import predict_disease

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form['symptoms']
    result = predict_disease(symptoms)
    return render_template("index.html", prediction=result)

if __name__ == '__main__':
    app.run(debug=True)
