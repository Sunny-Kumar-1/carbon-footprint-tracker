import os
import sys
import json

# Add project root to sys path to import core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator
from core.predict import CarbonPredictor

OPTIONS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core', 'options.json')

def load_options():
    with open(OPTIONS_PATH, 'r') as f:
        return json.load(f)

def run_cli():
    print("Welcome to the Carbon Footprint Tracker CLI!")
    print("Please answer a few questions to estimate your monthly carbon footprint.\n")
    
    options = load_options()
    user_data = {}
    
    # Categorical Questions
    for feature, choices in options['categorical'].items():
        user_data[feature] = inquirer.select(
            message=f"Select your {feature}:",
            choices=choices,
        ).execute()
        
    # Numeric Questions
    for feature, stats in options['numeric'].items():
        min_val = stats['min']
        max_val = stats['max']
        
        # FloatValidator or just custom validation 
        val_str = inquirer.text(
            message=f"Enter your {feature} (min: {min_val}, max: {max_val}):",
            validate=NumberValidator(float_allowed=True),
            filter=lambda result: float(result)
        ).execute()
        
        user_data[feature] = val_str
        
    print("\nCalculating your footprint...")
    predictor = CarbonPredictor()
    try:
        footprint = predictor.predict(user_data)
        print(f"\n=> Your estimated Carbon Footprint is: {footprint:.2f} kg CO2 emission per month/year (based on dataset metric).")
    except Exception as e:
        print(f"\nError calculating footprint: {e}")

if __name__ == "__main__":
    run_cli()
