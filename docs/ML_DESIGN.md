# 🎯 Machine Learning Design Document

## Overview

This document explains the machine learning design decisions and methodology used in the House Price Prediction Platform.

## Problem Statement

Predict house prices based on multiple features using regression techniques, providing accurate estimates with confidence intervals.

## Dataset Requirements

### Expected Features

| Feature | Type | Description | Range |
|---------|------|-------------|-------|
| area | Numerical | Living area in square feet | > 0 |
| bedrooms | Numerical | Number of bedrooms | 0-20 |
| bathrooms | Numerical | Number of bathrooms | 0-20 |
| location | Categorical | Neighborhood/area name | String |
| year_built | Numerical | Year of construction | 1800-2030 |
| price | Numerical | Target variable (house price) | > 0 |

### Data Quality Requirements

- **Completeness**: < 10% missing values per feature
- **Size**: Minimum 500 samples recommended
- **Distribution**: Reasonably normal distribution for price
- **Outliers**: Will be handled via Z-score method

## Data Preprocessing Pipeline

### 1. Missing Value Handling

**Strategy:**
- **Numerical features**: Median imputation
- **Categorical features**: Mode imputation

**Rationale**: Median is robust to outliers, mode preserves categorical distribution.

### 2. Outlier Detection

**Method**: Z-score with threshold = 3 standard deviations

**Process**:
```python
z_score = (value - mean) / std
if |z_score| > 3: remove sample
```

**Rationale**: Removes extreme values that could skew model training while preserving 99.7% of normal data.

### 3. Feature Encoding

**Categorical Features**: Label Encoding

**Rationale**: 
- Simple and effective for tree-based models
- Preserves ordinality if present
- Minimal memory footprint

**Alternative Considered**: One-Hot Encoding (rejected due to potential high dimensionality)

### 4. Feature Scaling

**Method**: StandardScaler (Z-score normalization)

**Formula**:
```python
scaled_value = (value - mean) / std
```

**Rationale**:
- Required for Ridge and Lasso regression (L1/L2 regularization)
- Ensures all features contribute equally
- Improves convergence speed

## Model Selection

### Models Evaluated

#### 1. Linear Regression (Baseline)

**Pros**:
- Simple, interpretable
- Fast training
- No hyperparameters

**Cons**:
- No regularization
- Prone to overfitting with many features
- Sensitive to multicollinearity

#### 2. Ridge Regression (L2 Regularization)

**Formula**: 
```
Loss = MSE + α * Σ(β²)
```

**Pros**:
- Handles multicollinearity well
- Reduces overfitting
- Keeps all features

**Cons**:
- Requires hyperparameter tuning (α)
- Less interpretable than linear regression

**Hyperparameter**: α = 1.0 (default, can be tuned)

#### 3. Lasso Regression (L1 Regularization)

**Formula**:
```
Loss = MSE + α * Σ|β|
```

**Pros**:
- Feature selection (can zero out coefficients)
- Handles multicollinearity
- Sparse solutions

**Cons**:
- May remove important features
- Requires hyperparameter tuning (α)

**Hyperparameter**: α = 1.0 (default, can be tuned)

### Model Selection Criteria

**Method**: 5-Fold Cross-Validation

**Metric**: Root Mean Squared Error (RMSE)

**Process**:
1. Train each model with 5-fold CV
2. Calculate mean RMSE across folds
3. Select model with lowest mean RMSE
4. Retrain on full training set

**Rationale**: RMSE penalizes large errors more than MAE, which is important for price predictions.

## Evaluation Metrics

### 1. Mean Absolute Error (MAE)

```python
MAE = (1/n) * Σ|y_true - y_pred|
```

**Interpretation**: Average dollar amount of prediction error

**Target**: < 10% of mean price

### 2. Root Mean Squared Error (RMSE)

```python
RMSE = √[(1/n) * Σ(y_true - y_pred)²]
```

**Interpretation**: Standard deviation of prediction errors

**Target**: < 15% of mean price

### 3. R² Score (Coefficient of Determination)

```python
R² = 1 - (SS_res / SS_tot)
```

**Interpretation**: Proportion of variance explained by the model

**Target**: > 0.85

**Scale**: 
- 1.0 = Perfect predictions
- 0.0 = Model as good as mean baseline
- < 0.0 = Model worse than baseline

## Model Interpretability

### Feature Importance

For linear models, feature importance is determined by coefficient magnitude:

```python
importance = |coefficient| * std(feature)
```

### Prediction Confidence

**Confidence Interval Estimation**:
- Simple approach: ±5% of predicted value
- Advanced approach: Prediction intervals from model (future enhancement)

## Production Considerations

### Model Persistence

**Format**: Joblib (pickle-based)

**Artifacts Saved**:
1. `best_model.joblib` - Trained model
2. `scaler.joblib` - Fitted StandardScaler
3. `encoder.joblib` - Fitted LabelEncoders
4. `feature_names.joblib` - Feature order
5. `model_metadata.joblib` - Training metadata

### Inference Pipeline

```
Input → Encode Categories → Scale Features → Predict → Return Result
```

### Model Monitoring

**Metrics to Track**:
- Prediction latency
- Prediction distribution drift
- Error rates
- API uptime

### Model Retraining

**Triggers**:
- Performance degradation (R² < 0.80)
- Significant data drift
- New data availability
- Scheduled (e.g., quarterly)

## Limitations and Future Improvements

### Current Limitations

1. **Simple Feature Set**: Only 5 features used
2. **Linear Assumptions**: May not capture complex non-linear relationships
3. **No Feature Engineering**: No interaction terms or polynomial features
4. **Basic Confidence Intervals**: Simple ±5% approximation

### Future Enhancements

1. **Additional Features**:
   - Property age (derived from year_built)
   - Price per square foot
   - Neighborhood statistics
   - Proximity to amenities

2. **Advanced Models**:
   - Gradient Boosting (XGBoost, LightGBM)
   - Random Forest
   - Neural Networks

3. **Feature Engineering**:
   - Polynomial features
   - Interaction terms
   - Binning/discretization

4. **Better Uncertainty Estimation**:
   - Quantile regression
   - Conformal prediction
   - Bayesian approaches

5. **Hyperparameter Optimization**:
   - Grid search
   - Random search
   - Bayesian optimization

## References

- Scikit-learn Documentation: https://scikit-learn.org/
- "An Introduction to Statistical Learning" - James, Witten, Hastie, Tibshirani
- "Hands-On Machine Learning" - Aurélien Géron

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-10  
**Author**: ML Engineering Team
