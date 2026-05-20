import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import os

def train_and_save_model(csv_path: str, model_save_path: str):
    print("Loading dataset...")
    df = pd.read_csv(csv_path)

    # Some of the categorical list strings look like "['Metal']" or "['Stove', 'Oven']"
    # For a simple baseline, we'll just treat the entire string as a category
    # to avoid complex parsing right now. 
    
    # Target Variable
    target = 'CarbonEmission'
    
    # Features
    X = df.drop(columns=[target])
    y = df[target]

    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    numeric_features = X.select_dtypes(exclude=['object']).columns.tolist()

    # Create preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Append regressor to preprocessing pipeline
    # Now we have a full prediction pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training model...")
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    print(f"Model trained! Test R^2 Score: {score:.4f}")

    print(f"Saving model to {model_save_path}...")
    joblib.dump(clf, model_save_path)
    print("Done!")

if __name__ == "__main__":
    dataset_path = 'c:/PROJECT/Carbon Emission.csv/Carbon Emission.csv'
    model_path = 'c:/PROJECT/carbon-footprint-tracker/core/model.pkl'
    train_and_save_model(dataset_path, model_path)
