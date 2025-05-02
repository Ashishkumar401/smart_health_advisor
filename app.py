from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from ml_model import predict_disease  # Ensure this exists

app = Flask(__name__)

# Set base path for datasets
base_path = 'C:/Users/HP/OneDrive/Desktop/smart_health_advisor/data/'

# Load datasets
doctor_mapping_df = pd.read_csv(os.path.join(base_path, 'Doctor_Versus_Disease.csv'), encoding='latin1', names=['Disease', 'Doctor'], header=None)
doctor_mapping_df.columns = doctor_mapping_df.columns.str.strip()
doctor_specialist_df = pd.read_csv(os.path.join(base_path, 'Doctor_Specialist.csv'), encoding='latin1')
disease_description_df = pd.read_csv(os.path.join(base_path, 'Disease_Description.csv'), encoding='latin1')
symptom_weights_df = pd.read_csv(os.path.join(base_path, 'Symptom_Weights.csv'), encoding='latin1')
zocdoc_df = pd.read_csv(os.path.join(base_path, 'zocdoc.csv'), encoding='utf-8')
zocdoc_df.columns = zocdoc_df.columns.str.strip()

# ✅ Home page
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Disease prediction
@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.form.get('symptoms')
    if symptoms:
        symptom_list = symptoms.lower().replace(" ", "").split(',')
        disease, prob = predict_disease(symptom_list)
        recommended_doctors = doctor_mapping_df[doctor_mapping_df['Disease'] == disease]['Doctor'].tolist()
        return render_template('result.html', disease=disease, probability=round(prob * 100, 2), doctors=recommended_doctors)
    else:
        return "No symptoms provided!"

# ✅ Smart chatbot route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json['message'].lower()

    # Smart response logic
    responses = {
        "chest pain": "Chest pain can be serious...",
        "headache": "Headaches are often due to stress...",
        "fever": "Fever may indicate an infection...",
        # ... (add remaining 50+ responses here)
        "mouth ulcers": "Caused by vitamin deficiency or stress..."
    }

    reply = "Can you tell me more about your symptoms?"
    for keyword in responses:
        if keyword in user_message:
            reply = responses[keyword]
            break

    return jsonify({'reply': reply})

# ✅ Symptom Severity Visualization
@app.route("/visualize_symptoms")
def visualize_symptoms():
    df = pd.read_csv(os.path.join(base_path, 'Symptom_Weights.csv'), header=None, names=["Symptom", "Weight"])
    df_sorted = df.sort_values(by="Weight", ascending=False)

    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure(figsize=(10, 30))
    sns.barplot(x="Weight", y="Symptom", data=df_sorted, palette="Reds_r")
    plt.title("Symptom Severity Visualization")
    plt.xlabel("Symptom Weight")
    plt.ylabel("Symptom")
    plt.tight_layout()
    plt.savefig("static/symptom_plot.png")
    plt.close()

    return render_template("symptom_plot.html")

# ✅ Search doctor by specialization with bar graph
@app.route('/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    result = []
    message = ""
    if request.method == 'POST':
        specialty = request.form.get('specialty', '').lower()
        if specialty:
            filtered = zocdoc_df[zocdoc_df['speciality'].str.lower().str.contains(specialty)]
            result = filtered[["Doctor's Name", 'speciality']].values.tolist()
            if not result:
                message = f"No doctors found for specialization: {specialty}"
        else:
            message = "Specialization not provided!"

    # Plot doctor count by specialization
    count_df = zocdoc_df['speciality'].value_counts().reset_index()
    count_df.columns = ['Speciality', 'Doctor Count']

    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Doctor Count', y='Speciality', data=count_df.head(10), palette='Blues_r')
    plt.title("Top 10 Specializations by Number of Doctors")
    plt.tight_layout()
    plt.savefig('static/doctor_speciality_bar.png')
    plt.close()

    return render_template('search_doctor.html', result=result, message=message, bar_image='doctor_speciality_bar.png')

# ✅ API: Get doctors by specialization
@app.route('/get_doctors/<speciality>')
def get_doctors_by_speciality(speciality):
    doctors = zocdoc_df[zocdoc_df['speciality'].str.lower() == speciality.lower()]["Doctor's Name"].tolist()
    return jsonify({'doctors': doctors})

# ✅ Chat page route
@app.route('/chat')
def chat_page():
    return render_template('chat.html')

# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)
