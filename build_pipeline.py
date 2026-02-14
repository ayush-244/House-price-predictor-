"""
House Price Prediction Build Pipeline
Cleans data, augments it with synthetic records for India, and trains the model.
"""

import pandas as pd
import numpy as np
import json
import joblib
import os
import logging
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Set up logging for tracking progress
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory configuration
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "ml" / "data"
MODELS_DIR = BASE_DIR / "ml" / "models"
BACKEND_DATA_DIR = BASE_DIR / "backend" / "app" / "data"

# Ensure required directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
BACKEND_DATA_DIR.mkdir(parents=True, exist_ok=True)

def run_pipeline():
    logger.info("Starting pipeline execution")

    # Phase 1: Clean original raw data
    logger.info("Loading original dataset...")
    try:
        df_orig = pd.read_csv("india_housing_prices.csv")
    except FileNotFoundError:
        logger.error("Dataset not found!")
        return

    # Basic data cleaning and renaming
    df_clean = pd.DataFrame()
    df_clean['area'] = df_orig['Size_in_SqFt']
    df_clean['bedrooms'] = df_orig['BHK']
    df_clean['bathrooms'] = df_clean['bedrooms'].apply(lambda x: min(x, 5))
    df_clean['state'] = df_orig['State'].str.strip()
    df_clean['location'] = df_orig['City'].str.strip()
    
    # Generate realistic built years
    np.random.seed(42)
    df_clean['year_built'] = np.random.randint(2005, 2024, size=len(df_clean))
    
    # Map property types based on room counts
    def get_prop_type(bhk):
        if bhk <= 2: return "Apartment"
        if bhk == 3: return np.random.choice(["Apartment", "Independent House"], p=[0.7, 0.3])
        return np.random.choice(["Independent House", "Villa"], p=[0.7, 0.3])
    
    df_clean['property_type'] = df_clean['bedrooms'].apply(get_prop_type)
    
    # Assign parking based on property type
    def get_parking(row):
        if row['property_type'] in ['Villa', 'Independent House']: return 1
        return np.random.choice([0, 1])
    
    df_clean['parking'] = df_clean.apply(get_parking, axis=1)

    # Assign modular kitchen and dining hall features
    df_clean['modular_kitchen'] = np.random.choice([0, 1], size=len(df_clean), p=[0.4, 0.6])
    
    def get_dining(row):
        if row['bedrooms'] >= 3 or row['area'] > 1200:
            return np.random.choice([0, 1], p=[0.2, 0.8])
        return np.random.choice([0, 1], p=[0.8, 0.2])
        
    df_clean['dining_hall'] = df_clean.apply(get_dining, axis=1)
    
    # Convert price to absolute rupees
    df_clean['price'] = df_orig['Price_in_Lakhs'] * 100000
    logger.info(f"Cleaned {len(df_clean)} records.")

    # Phase 2: Create synthetic data for full India coverage
    try:
        with open('indian_districts.json', 'r') as f:
            districts_data = json.load(f)
    except FileNotFoundError:
        logger.error("District mapping file missing!")
        return

    # Calculate price per square foot for baseline
    avg_price_sqft = (df_clean['price'] / df_clean['area']).mean()
    logger.info(f"Baseline: ₹{avg_price_sqft:.0f}/sqft")

    # City tiers for price multipliers
    tier1 = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Gurgaon", "Noida"]
    tier2 = ["Jaipur", "Lucknow", "Chandigarh", "Indore", "Nagpur", "Thane", "Bhopal", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Coimbatore", "Visakhapatnam", "Kochi", "Raipur", "Bhubaneswar"]

    new_records = []
    for state_obj in districts_data['states']:
        state = state_obj['state']
        for city in state_obj['districts']:
            # Skip if we already have data
            if len(df_clean[(df_clean['state'] == state) & (df_clean['location'] == city)]) > 50:
                continue
            
            # Tier-based price multiplier
            mult = 0.5
            if any(t.lower() in city.lower() for t in tier1): mult = 1.8
            elif any(t.lower() in city.lower() for t in tier2): mult = 1.1
            
            # Generate sample records
            for _ in range(100):
                area = max(400, min(int(np.random.normal(1200, 400)), 4000))
                bhk = np.random.choice([1, 2, 3, 4], p=[0.2, 0.4, 0.3, 0.1])
                bath = min(bhk, 4)
                ptype = np.random.choice(['Apartment', 'Independent House', 'Villa'], p=[0.6, 0.3, 0.1] if mult > 1.0 else [0.3, 0.6, 0.1])
                parking = 1 if ptype == 'Villa' else np.random.randint(0, 2)
                year = np.random.randint(2010, 2024)
                mod_kit = int(np.random.choice([0, 1], p=[0.4, 0.6]))
                dining = 1 if (bhk >= 3 or area > 1200) else int(np.random.choice([0, 1], p=[0.8, 0.2]))
                
                # Dynamic pricing logic
                type_mult = {'Apartment': 1.0, 'Independent House': 1.15, 'Villa': 1.4}
                park_mult = 1.05 if parking else 1.0
                kit_mult = 1.05 if mod_kit else 1.0
                din_mult = 1.03 if dining else 1.0
                
                est_price = (area * avg_price_sqft * mult) * type_mult[ptype] * park_mult * kit_mult * din_mult
                est_price *= np.random.uniform(0.85, 1.15)
                
                new_records.append({
                    'area': area, 'bedrooms': bhk, 'bathrooms': bath, 'state': state,
                    'location': city, 'year_built': year, 'property_type': ptype,
                    'parking': parking, 'modular_kitchen': mod_kit, 'dining_hall': dining,
                    'price': int(est_price)
                })
    
    df_aug = pd.DataFrame(new_records)
    logger.info(f"Generated {len(df_aug)} synthetic records.")
    
    # Combine original and synthetic data
    df_final = pd.concat([df_clean, df_aug], ignore_index=True)
    df_final.dropna(inplace=True)
    
    # Save the prepared dataset
    csv_path = DATA_DIR / "housing_data_final.csv"
    df_final.to_csv(csv_path, index=False)
    logger.info(f"Final dataset saved with {len(df_final)} rows.")

    # Phase 3: Train the ML Model
    logger.info("Training model...")
    cat_cols = ['state', 'location', 'property_type']
    num_cols = ['area', 'bedrooms', 'bathrooms', 'year_built', 'parking', 'modular_kitchen', 'dining_hall']
    
    # Label encode categorical strings
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df_final[col] = df_final[col].astype(str)
        df_final[col] = le.fit_transform(df_final[col])
        encoders[col] = le
    
    X = df_final[num_cols + cat_cols]
    y = df_final['price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale numerical features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Fit the regressor
    model = RandomForestRegressor(n_estimators=100, max_depth=20, n_jobs=-1, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate performance
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    logger.info(f"R² Score: {r2:.4f}, RMSE: ₹{rmse:,.0f}")

    # Phase 4: Save trained artifacts
    logger.info("Saving artifacts...")
    joblib.dump(model, MODELS_DIR / "best_model.joblib")
    joblib.dump(scaler, MODELS_DIR / "scaler.joblib")
    joblib.dump(encoders, MODELS_DIR / "encoder.joblib")
    joblib.dump(list(X.columns), MODELS_DIR / "feature_names.joblib")
    
    metadata = {
        "accuracy": r2,
        "rmse": rmse,
        "timestamp": datetime.now().isoformat()
    }
    joblib.dump(metadata, MODELS_DIR / "model_metadata.joblib")
    logger.info("Artifacts saved successfully.")

    # Phase 5: Prepare frontend data mappings
    logger.info("Generating frontend mapping files...")
    df_saved = pd.read_csv(csv_path)
    location_mapping = {}
    states = sorted(df_saved['state'].unique())
    for s in states:
        cities = sorted(df_saved[df_saved['state'] == s]['location'].unique())
        location_mapping[s] = cities
        
    with open(BACKEND_DATA_DIR / "location_mapping.json", "w") as f:
        json.dump(location_mapping, f, indent=2)
    logger.info("Location mapping generated.")

    # Run verification check
    logger.info("Running verification...")
    try:
        m = joblib.load(MODELS_DIR / "best_model.joblib")
        s = joblib.load(MODELS_DIR / "scaler.joblib")
        e = joblib.load(MODELS_DIR / "encoder.joblib")
        fn = joblib.load(MODELS_DIR / "feature_names.joblib")
        
        test_input = pd.DataFrame([{
            'area': 2000, 'bedrooms': 3, 'bathrooms': 2, 'year_built': 2018,
            'parking': 0, 'modular_kitchen': 0, 'dining_hall': 0,
            'state': 'Uttar Pradesh', 'location': 'Varanasi',
            'property_type': 'Independent House'
        }])
        
        for col in cat_cols:
            test_input[col] = e[col].transform(test_input[col])
            
        test_scaled = s.transform(test_input[fn])
        pred = m.predict(test_scaled)[0]
        logger.info(f"Verification successful. Pred price: ₹{pred:,.0f}")
        
    except Exception as ex:
        logger.error(f"Verification failed: {ex}")

    logger.info("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()


    



    
