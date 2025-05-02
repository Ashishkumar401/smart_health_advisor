import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Dummy data (aap yeh baad mein original data se replace kar sakte hain)
data = {
    'fever': [1, 0, 1, 0],
    'cough': [1, 1, 0, 0],
    'headache': [0, 1, 1, 0],
    'disease': ['Flu', 'Cold', 'Migraine', 'Healthy']
}

df = pd.DataFrame(data)

# X = features, y = label
X = df[['fever', 'cough', 'headache']]
y = df['disease']

# Random Forest model train karna
model = RandomForestClassifier()
model.fit(X, y)

# models folder banana agar nahi bana hai to
model_dir = 'models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Model ko pickle file mein save karna
model_path = os.path.join(model_dir, 'rf_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"Model saved to {model_path}")
