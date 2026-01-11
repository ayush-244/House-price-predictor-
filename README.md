# 🏠 House Price Prediction Platform

A production-ready machine learning system for predicting house prices using multivariate regression, built with modern engineering practices.

## 📋 System Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  React Frontend │ ───> │  FastAPI Backend│ ───> │   ML Model      │
│  (Port 3000)    │ <─── │  (Port 8000)    │ <─── │   (joblib)      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

## 🎯 Features

### Machine Learning Layer
- **Multiple Models**: Linear, Ridge, and Lasso Regression
- **Robust Preprocessing**: Missing values, outliers, encoding, scaling
- **Model Selection**: Cross-validation based selection
- **Evaluation Metrics**: MAE, RMSE, R²
- **Model Persistence**: Joblib serialization

### Backend API
- **FastAPI Framework**: High-performance async API
- **Input Validation**: Pydantic schemas
- **Error Handling**: Structured error responses
- **API Documentation**: Auto-generated Swagger UI
- **Health Monitoring**: Service health endpoint

### Frontend UI
- **Modern React**: Component-based architecture
- **Responsive Design**: Mobile and desktop optimized
- **Real-time Validation**: Form input validation
- **Loading States**: User feedback during predictions
- **Professional UI**: Clean, intuitive interface

## 📁 Project Structure

```
house-price-prediction/
├── ml/                          # Machine Learning Pipeline
│   ├── data/                    # Dataset storage
│   ├── models/                  # Trained models
│   ├── notebooks/               # Exploratory analysis
│   ├── src/
│   │   ├── data_preprocessing.py
│   │   ├── model_training.py
│   │   ├── model_evaluation.py
│   │   └── config.py
│   └── requirements.txt
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   ├── schemas/
│   │   │   └── prediction.py
│   │   ├── services/
│   │   │   └── prediction_service.py
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── frontend/                    # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── index.jsx
│   └── package.json
│
└── docs/                        # Documentation
    ├── API.md
    └── ML_DESIGN.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### 1️⃣ Setup ML Pipeline

```bash
cd ml
pip install -r requirements.txt

# Place your dataset in ml/data/housing_data.csv
# Then train the model
python src/model_training.py
```

### 2️⃣ Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API will be available at: http://localhost:8000
Swagger docs at: http://localhost:8000/docs

### 3️⃣ Start Frontend

```bash
cd frontend
npm install
npm start
```

Frontend will be available at: http://localhost:3000

## 📊 ML Model Details

### Features Used
- **Area (sqft)**: Living area in square feet
- **Bedrooms**: Number of bedrooms
- **Bathrooms**: Number of bathrooms
- **Location**: Categorical location feature
- **Year Built**: Construction year

### Models Compared
1. **Linear Regression**: Baseline model
2. **Ridge Regression**: L2 regularization
3. **Lasso Regression**: L1 regularization (feature selection)

### Model Selection
- 5-fold cross-validation
- Best model selected based on lowest RMSE
- Final evaluation on test set (20% split)

## 🔌 API Endpoints

### POST /predict
Predict house price based on features.

**Request Body:**
```json
{
  "area": 2500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "Downtown",
  "year_built": 2010
}
```

**Response:**
```json
{
  "predicted_price": 450000.50,
  "model_used": "Ridge Regression",
  "confidence_interval": {
    "lower": 430000,
    "upper": 470000
  }
}
```

### GET /health
Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-01-10T22:37:22Z"
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔧 Configuration

### Environment Variables

Create `.env` files in respective directories:

**backend/.env**
```
MODEL_PATH=../ml/models/best_model.joblib
SCALER_PATH=../ml/models/scaler.joblib
ENCODER_PATH=../ml/models/encoder.joblib
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

**frontend/.env**
```
REACT_APP_API_URL=http://localhost:8000
```

## 📈 Performance Metrics

Expected model performance (will vary based on dataset):
- **R² Score**: > 0.85
- **RMSE**: < 15% of mean price
- **MAE**: < 10% of mean price

## 🛠️ Tech Stack

### ML & Backend
- **Python 3.8+**
- **scikit-learn**: ML models
- **pandas**: Data manipulation
- **FastAPI**: API framework
- **Pydantic**: Data validation
- **uvicorn**: ASGI server
- **joblib**: Model serialization

### Frontend
- **React 18**: UI framework
- **Axios**: HTTP client
- **CSS3**: Styling
- **React Hooks**: State management

## 📝 Development Workflow

1. **Data Exploration**: Analyze dataset in Jupyter notebooks
2. **Feature Engineering**: Create and select features
3. **Model Training**: Train and compare models
4. **Model Evaluation**: Validate performance
5. **API Development**: Build FastAPI endpoints
6. **Frontend Development**: Create React UI
7. **Integration Testing**: End-to-end testing
8. **Deployment**: Deploy to production

## 🚢 Deployment

### Backend Deployment (Docker)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
COPY ml/models/ ./models/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy build/ folder to static hosting (Netlify, Vercel, etc.)
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

Built with ❤️ following production ML engineering best practices.

## 🙏 Acknowledgments

- Dataset: [Will be specified once provided]
- Inspired by real-world ML systems at scale
- Built for learning and production use

---

**Note**: This is a production-oriented implementation suitable for real-world deployment while remaining accessible to motivated beginners.
