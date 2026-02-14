# 📊 Dataset Instructions

## Required Dataset Format

Your Kaggle dataset should be a CSV file with the following columns:

### Required Columns

| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| `area` | Numeric | Living area in square feet | 1200, 2500, 3400 |
| `bedrooms` | Integer | Number of bedrooms | 2, 3, 4 |
| `bathrooms` | Numeric | Number of bathrooms | 1, 2.5, 3 |
| `location` | String | Neighborhood/area name | "Downtown", "Suburb", "Rural" |
| `year_built` | Integer | Year of construction | 1990, 2005, 2015 |
| `price` | Numeric | House price (target variable) | 250000, 450000, 750000 |

## Setup Instructions

1. **Download your dataset from Kaggle**
   - Go to your chosen Kaggle dataset
   - Download the CSV file

2. **Prepare the dataset**
   - Ensure it has the required columns listed above
   - If column names are different, rename them to match
   - Save as `housing_data.csv`

3. **Place the dataset**
   - Copy `housing_data.csv` to: `ml/data/housing_data.csv`

4. **Verify the dataset**
   ```python
   import pandas as pd
   df = pd.read_csv('ml/data/housing_data.csv')
   print(df.head())
   print(df.info())
   ```

## Column Mapping Examples

If your Kaggle dataset has different column names, here's how to rename them:

### Example 1: California Housing Dataset
```python
import pandas as pd

df = pd.read_csv('original_dataset.csv')
df = df.rename(columns={
    'sqft_living': 'area',
    'bedrooms': 'bedrooms',
    'bathrooms': 'bathrooms',
    'city': 'location',
    'yr_built': 'year_built',
    'price': 'price'
})
df.to_csv('ml/data/housing_data.csv', index=False)
```

### Example 2: Generic Housing Dataset
```python
import pandas as pd

df = pd.read_csv('original_dataset.csv')

# Select and rename columns
df_prepared = pd.DataFrame({
    'area': df['square_feet'],
    'bedrooms': df['bed'],
    'bathrooms': df['bath'],
    'location': df['neighborhood'],
    'year_built': df['year'],
    'price': df['sale_price']
})

df_prepared.to_csv('ml/data/housing_data.csv', index=False)
```

## Data Quality Checks

Before training, ensure:

✅ **No duplicate rows**
```python
print(f"Duplicates: {df.duplicated().sum()}")
df = df.drop_duplicates()
```

✅ **Reasonable value ranges**
```python
print(df.describe())
# Check for negative values, extreme outliers
```

✅ **Sufficient data**
```python
print(f"Total samples: {len(df)}")
# Recommended: At least 500 samples
```

✅ **Missing values are acceptable**
```python
print(df.isnull().sum())
# < 10% missing per column is fine (will be handled by preprocessing)
```

## Popular Kaggle Datasets

Here are some recommended datasets:

1. **House Prices - Advanced Regression Techniques**
   - URL: https://www.kaggle.com/c/house-prices-advanced-regression-techniques
   - Features: 79 features including area, bedrooms, etc.

2. **USA Housing Dataset**
   - URL: https://www.kaggle.com/datasets/vedavyasv/usa-housing
   - Features: Area, bedrooms, bathrooms, etc.

3. **California Housing Prices**
   - URL: https://www.kaggle.com/datasets/camnugent/california-housing-prices
   - Features: Median house values, rooms, location

## After Placing the Dataset

Once you've placed `housing_data.csv` in `ml/data/`, you can:

1. **Train the model**:
   ```bash
   cd ml
   python src/model_training.py
   ```

2. **Evaluate the model**:
   ```bash
   python src/model_evaluation.py
   ```

3. **Start the backend**:
   ```bash
   cd ../backend
   uvicorn app.main:app --reload
   ```

## Need Help?

If you encounter issues:
- Check that column names match exactly
- Verify data types are correct
- Look for any special characters in location names
- Ensure price values are numeric (no currency symbols)

---

**Ready to proceed?** Just let me know when you've placed the dataset, and I'll help you train the model!
