import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

class CarbonPredictor:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        if self.model is None:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run train.py first.")
            self.model = joblib.load(MODEL_PATH)

    def predict(self, user_data: dict) -> float:
        """
        Predict carbon footprint based on user inputs.
        user_data should be a dictionary containing all features expected by the model.
        """
        self.load_model()
        # Convert single dict to DataFrame for prediction
        df = pd.DataFrame([user_data])
        prediction = self.model.predict(df)
        return prediction[0]
