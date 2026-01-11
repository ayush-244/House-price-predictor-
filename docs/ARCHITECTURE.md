# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REACT FRONTEND                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Header     │  │ Prediction   │  │   Footer     │          │
│  │  Component   │  │     Form     │  │  Component   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                             │                                    │
│                    ┌────────▼────────┐                          │
│                    │   API Service   │                          │
│                    │   (Axios)       │                          │
│                    └─────────────────┘                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ POST /api/v1/predict
                             │ GET  /api/v1/health
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                   http://localhost:8000                          │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                    API Routes                         │       │
│  │  • POST /predict    • GET /health    • GET /model-info│       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│  ┌────────────────────────▼─────────────────────────────┐       │
│  │              Prediction Service                       │       │
│  │  • Load Model    • Preprocess    • Predict           │       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│  ┌────────────────────────▼─────────────────────────────┐       │
│  │              Pydantic Schemas                         │       │
│  │  • Input Validation    • Response Formatting         │       │
│  └───────────────────────────────────────────────────────┘       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Load Models
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ML MODELS (Joblib Files)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Best Model   │  │   Scaler     │  │   Encoders   │          │
│  │  .joblib     │  │   .joblib    │  │   .joblib    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                             ▲
                             │
                             │ Training Process
                             │
┌─────────────────────────────────────────────────────────────────┐
│                    ML TRAINING PIPELINE                          │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  1. Data Loading (CSV)                               │       │
│  │     └─> housing_data.csv                             │       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│  ┌────────────────────────▼─────────────────────────────┐       │
│  │  2. Data Preprocessing                                │       │
│  │     • Handle Missing Values                          │       │
│  │     • Remove Outliers (Z-score)                      │       │
│  │     • Encode Categories (Label Encoding)             │       │
│  │     • Scale Features (StandardScaler)                │       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│  ┌────────────────────────▼─────────────────────────────┐       │
│  │  3. Model Training & Selection                        │       │
│  │     • Linear Regression                              │       │
│  │     • Ridge Regression                               │       │
│  │     • Lasso Regression                               │       │
│  │     • 5-Fold Cross-Validation                        │       │
│  │     • Select Best Model (Lowest RMSE)                │       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│  ┌────────────────────────▼─────────────────────────────┐       │
│  │  4. Model Evaluation                                  │       │
│  │     • Calculate MAE, RMSE, R²                        │       │
│  │     • Generate Plots                                 │       │
│  │     • Save Evaluation Report                         │       │
│  └────────────────────────┬─────────────────────────────┘       │
│                           │                                      │
│  ┌────────────────────────▼─────────────────────────────┐       │
│  │  5. Model Persistence                                 │       │
│  │     • Save Best Model                                │       │
│  │     • Save Preprocessors                             │       │
│  │     • Save Metadata                                  │       │
│  └───────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Training Flow
```
CSV Dataset
    │
    ├─> Load Data
    │
    ├─> Preprocess
    │   ├─> Handle Missing Values
    │   ├─> Remove Outliers
    │   ├─> Encode Categories
    │   └─> Scale Features
    │
    ├─> Train Models
    │   ├─> Linear Regression
    │   ├─> Ridge Regression
    │   └─> Lasso Regression
    │
    ├─> Cross-Validate
    │   └─> Select Best Model
    │
    ├─> Evaluate
    │   ├─> Calculate Metrics
    │   └─> Generate Plots
    │
    └─> Save
        ├─> Model (.joblib)
        ├─> Scaler (.joblib)
        ├─> Encoders (.joblib)
        └─> Metadata (.joblib)
```

### Prediction Flow
```
User Input (Frontend)
    │
    ├─> Validate Form
    │
    ├─> Send to API
    │   └─> POST /api/v1/predict
    │
    ├─> Backend Processing
    │   ├─> Validate with Pydantic
    │   ├─> Load Model & Preprocessors
    │   ├─> Encode Categories
    │   ├─> Scale Features
    │   └─> Make Prediction
    │
    ├─> Format Response
    │   ├─> Predicted Price
    │   ├─> Confidence Interval
    │   └─> Model Name
    │
    └─> Display Result (Frontend)
        ├─> Show Price
        ├─> Show Confidence Range
        └─> Show Model Used
```

## Component Interactions

### Frontend Components
```
App.jsx (Main Container)
    │
    ├─> Header.jsx
    │   └─> Logo & Branding
    │
    ├─> PredictionForm.jsx
    │   ├─> Form Inputs
    │   ├─> Validation
    │   ├─> API Calls (via api.js)
    │   └─> Result Display
    │
    └─> Footer.jsx
        └─> Information & Links
```

### Backend Components
```
main.py (FastAPI App)
    │
    ├─> Middleware
    │   ├─> CORS
    │   └─> Request Logging
    │
    ├─> Routes (routes.py)
    │   ├─> /predict
    │   ├─> /health
    │   └─> /model-info
    │
    ├─> Services
    │   └─> prediction_service.py
    │       ├─> load_model()
    │       ├─> preprocess_input()
    │       └─> predict()
    │
    └─> Schemas (prediction.py)
        ├─> HouseFeaturesInput
        ├─> PredictionResponse
        └─> HealthResponse
```

## Technology Stack Details

### Frontend Stack
```
React 18.2.0
    ├─> Vite (Build Tool)
    ├─> Axios (HTTP Client)
    └─> Modern CSS3
        ├─> Gradients
        ├─> Animations
        └─> Responsive Design
```

### Backend Stack
```
FastAPI 0.109.0
    ├─> Uvicorn (ASGI Server)
    ├─> Pydantic (Validation)
    └─> Python 3.8+
```

### ML Stack
```
scikit-learn 1.3.2
    ├─> Regression Models
    ├─> Preprocessing
    └─> Cross-Validation
    
pandas 2.1.4
    └─> Data Manipulation
    
numpy 1.24.3
    └─> Numerical Operations
    
joblib 1.3.2
    └─> Model Persistence
```

## File Dependencies

### ML Pipeline Dependencies
```
model_training.py
    ├─> config.py (settings)
    ├─> data_preprocessing.py (preprocessing)
    └─> Outputs:
        ├─> best_model.joblib
        ├─> scaler.joblib
        ├─> encoder.joblib
        └─> model_metadata.joblib

model_evaluation.py
    ├─> config.py
    ├─> data_preprocessing.py
    ├─> model_training.py
    └─> Outputs:
        ├─> prediction_plot.png
        ├─> residual_plot.png
        └─> evaluation_report.txt
```

### Backend Dependencies
```
main.py
    ├─> routes.py
    │   └─> prediction_service.py
    │       ├─> config.py
    │       └─> prediction.py (schemas)
    └─> logging.py
```

### Frontend Dependencies
```
App.jsx
    ├─> Header.jsx
    ├─> PredictionForm.jsx
    │   ├─> api.js
    │   └─> helpers.js
    └─> Footer.jsx
```

## Port Configuration

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 8000 | http://localhost:8000 |
| Swagger Docs | 8000 | http://localhost:8000/docs |
| ReDoc | 8000 | http://localhost:8000/redoc |

## Environment Variables

### Backend (.env)
```
MODEL_PATH=../ml/models/best_model.joblib
SCALER_PATH=../ml/models/scaler.joblib
ENCODER_PATH=../ml/models/encoder.joblib
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
```

---

This architecture ensures:
- ✅ **Separation of Concerns**: ML, Backend, Frontend are independent
- ✅ **Scalability**: Each component can be scaled independently
- ✅ **Maintainability**: Clear structure and dependencies
- ✅ **Testability**: Each component can be tested in isolation
- ✅ **Production-Ready**: Follows industry best practices
