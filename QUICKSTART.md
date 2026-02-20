# 🚀 Quick Start Guide

This guide will help you get the House Price Prediction Platform up and running quickly.

## Prerequisites

Ensure you have the following installed:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)

Verify installations:
```bash
python --version
node --version
npm --version
```

## Step 1: Prepare Your Dataset

✅ **Done!** The dataset `india_housing_prices.csv` has been processed and is ready for use.
The processed file is located at `ml/data/housing_data.csv`.

You can re-process it anytime by running:
```bash
python prepare_dataset.py
```

## Step 2: Train the ML Model

Open a terminal in the project root directory:

```bash
# Navigate to ML directory
cd ml

# Install Python dependencies
pip install -r requirements.txt

# Train the model (this will take a few minutes)
python src/model_training.py

# Evaluate the model
python src/model_evaluation.py
```

✅ **Success indicators:**
- Model saved to `ml/models/best_model.joblib`
- Evaluation plots created in `ml/models/`
- Console shows R² score > 0.85

## Step 3: Start the Backend API

Open a **new terminal** window:

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --port 8000
```

✅ **Success indicators:**
- Console shows "Application startup complete!"
- API accessible at: http://localhost:8000
- Swagger docs at: http://localhost:8000/docs

## Step 4: Start the Frontend

Open **another new terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

✅ **Success indicators:**
- Console shows "Local: http://localhost:3000"
- Browser opens automatically
- You see the prediction form

## Step 5: Test the Application

1. **Open your browser** to http://localhost:3000
2. **Fill in the form** with sample data:
   - Area: 2500
   - Bedrooms: 3
   - Bathrooms: 2.5
   - Location: Downtown
   - Year Built: 2010
3. **Click "Get Prediction"**
4. **See the result** with predicted price and confidence interval

## Troubleshooting

### Model Not Found Error

**Problem**: Backend shows "Model file not found"

**Solution**: 
1. Ensure you've run `python src/model_training.py` in the `ml` directory
2. Check that `ml/models/best_model.joblib` exists

### Port Already in Use

**Problem**: "Address already in use" error

**Solution**:
```bash
# For backend (port 8000)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# For frontend (port 3000)
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### CORS Error

**Problem**: Frontend can't connect to backend

**Solution**:
1. Ensure backend is running on port 8000
2. Check `backend/app/core/config.py` has `http://localhost:3000` in CORS origins
3. Restart the backend server

### Dataset Format Error

**Problem**: "Missing required columns" error

**Solution**:
1. Check your CSV has all required columns
2. See `ml/data/README.md` for column mapping examples
3. Verify column names match exactly (case-sensitive)

## Next Steps

Once everything is running:

1. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Check Model Performance**: Review the plots in `ml/models/`
3. **Customize the UI**: Edit files in `frontend/src/components/`
4. **Add Features**: Extend the ML pipeline in `ml/src/`

## Development Workflow

### Making Changes to the Frontend
1. Edit files in `frontend/src/`
2. Changes auto-reload in the browser
3. Check console for errors

### Making Changes to the Backend
1. Edit files in `backend/app/`
2. Server auto-reloads (if using `--reload` flag)
3. Test changes at http://localhost:8000/docs

### Retraining the Model
1. Update dataset in `ml/data/`
2. Run `python src/model_training.py`
3. Restart backend to load new model

## Stopping the Application

To stop all services:

1. **Frontend**: Press `Ctrl+C` in the frontend terminal
2. **Backend**: Press `Ctrl+C` in the backend terminal
3. **Clean up**: No additional cleanup needed

## Production Deployment

For production deployment, see:
- `docs/DEPLOYMENT.md` (coming soon)
- Build frontend: `npm run build` in `frontend/`
- Use production ASGI server for backend
- Set `DEBUG=False` in backend `.env`

---

