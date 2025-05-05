import os
import pickle

model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'SSI_model.pkl')
with open(model_path, 'rb') as f:
    ssi_model = pickle.load(f)

def predict_ssi(features):
    return ssi_model.predict([features])[0]
