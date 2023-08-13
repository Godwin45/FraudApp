import joblib 
import numpy as np
import pandas as pd
from pathlib import Path



class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model_trainer/best_model.joblib'))

    
    def predict(self, data):
        prediction = self.model.predict(data)
        if prediction == 0:
            return "No Fraud"
        elif prediction == 1:
            return "Fraud"
        else:
            return "Unknown"  # Handle other cases if needed
