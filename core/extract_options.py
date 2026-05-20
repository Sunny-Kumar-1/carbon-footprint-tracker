import pandas as pd
import json
import os

def extract_options(csv_path: str, out_path: str):
    df = pd.read_csv(csv_path)
    target = 'CarbonEmission'
    df = df.drop(columns=[target])

    options = {"categorical": {}, "numeric": {}}
    
    cat_cols = df.select_dtypes(include=['object']).columns
    for c in cat_cols:
        options["categorical"][c] = df[c].dropna().unique().tolist()
        
    num_cols = df.select_dtypes(exclude=['object']).columns
    for c in num_cols:
        options["numeric"][c] = {
            "min": float(df[c].min()),
            "max": float(df[c].max()),
            "mean": float(df[c].mean())
        }
        
    with open(out_path, 'w') as f:
        json.dump(options, f, indent=2)

if __name__ == "__main__":
    extract_options('c:/PROJECT/Carbon Emission.csv/Carbon Emission.csv', 'c:/PROJECT/carbon-footprint-tracker/core/options.json')
