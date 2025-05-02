import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
import numpy as np

def predict_disease(symptom_list):
    model = joblib.load('model.pkl')
    mlb = joblib.load('mlb.pkl')
    
    input_data = mlb.transform([symptom_list])
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)
    
    save_prediction_graph(prediction_proba, model.classes_)
    return prediction[0], prediction_proba.max()

def save_prediction_graph(probas, classes):
    top_indices = np.argsort(probas[0])[::-1][:5]
    top_classes = [classes[i] for i in top_indices]
    top_probs = [probas[0][i] for i in top_indices]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(top_classes, top_probs, color='skyblue')
    plt.title("Top Disease Predictions")
    plt.xlabel("Diseases")
    plt.ylabel("Probability")
    plt.ylim(0, 1)

    for bar, prob in zip(bars, top_probs):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{prob:.2f}",
                 ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig("static/prediction.png")
    plt.close()
