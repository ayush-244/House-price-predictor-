# ✅ Setup Checklist

Use this checklist to ensure everything is set up correctly.

## 📋 Pre-Setup Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Git installed (optional, for version control)
- [ ] Code editor installed (VS Code, PyCharm, etc.)

## 📊 Dataset Preparation

- [ ] Downloaded housing dataset from Kaggle
- [ ] Dataset has required columns:
  - [ ] `area` (numeric)
  - [ ] `bedrooms` (integer)
  - [ ] `bathrooms` (numeric)
  - [ ] `location` (string)
  - [ ] `year_built` (integer)
  - [ ] `price` (numeric - target)
- [ ] Dataset saved as `housing_data.csv`
- [ ] File placed in `ml/data/housing_data.csv`
- [ ] Verified dataset format: `head ml/data/housing_data.csv`

## 🤖 ML Pipeline Setup

- [ ] Navigated to `ml` directory
- [ ] Created virtual environment (recommended):
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  ```
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Verified imports work: `python -c "import sklearn, pandas, numpy"`
- [ ] Ran model training: `python src/model_training.py`
- [ ] Training completed successfully
- [ ] Model files created in `ml/models/`:
  - [ ] `best_model.joblib`
  - [ ] `scaler.joblib`
  - [ ] `encoder.joblib`
  - [ ] `feature_names.joblib`
  - [ ] `model_metadata.joblib`
- [ ] Ran model evaluation: `python src/model_evaluation.py`
- [ ] Evaluation plots created:
  - [ ] `prediction_plot.png`
  - [ ] `residual_plot.png`
  - [ ] `evaluation_report.txt`
- [ ] Checked R² score > 0.70 (preferably > 0.85)

## 🔧 Backend Setup

- [ ] Navigated to `backend` directory
- [ ] Created virtual environment (if not using global):
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  ```
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Verified FastAPI installed: `python -c "import fastapi"`
- [ ] Created `.env` file (optional, or use defaults)
- [ ] Started backend: `uvicorn app.main:app --reload --port 8000`
- [ ] Backend started successfully
- [ ] Checked console for "Application startup complete!"
- [ ] Verified model loaded: Check logs for "Model loaded successfully"
- [ ] Tested health endpoint: http://localhost:8000/api/v1/health
- [ ] Accessed Swagger docs: http://localhost:8000/docs
- [ ] Tested prediction endpoint in Swagger UI

## 🎨 Frontend Setup

- [ ] Navigated to `frontend` directory
- [ ] Installed dependencies: `npm install`
- [ ] Installation completed without errors
- [ ] Created `.env` file (optional):
  ```
  VITE_API_URL=http://localhost:8000/api/v1
  ```
- [ ] Started dev server: `npm run dev`
- [ ] Frontend started successfully
- [ ] Browser opened automatically to http://localhost:3000
- [ ] Page loads without errors
- [ ] No console errors in browser DevTools

## 🧪 Integration Testing

- [ ] All three services running simultaneously:
  - [ ] ML models trained and saved
  - [ ] Backend API running on port 8000
  - [ ] Frontend running on port 3000
- [ ] Tested prediction flow:
  - [ ] Filled in form with sample data
  - [ ] Clicked "Get Prediction"
  - [ ] Received prediction result
  - [ ] Price displayed correctly
  - [ ] Confidence interval shown
  - [ ] Model name displayed
- [ ] Tested error handling:
  - [ ] Submitted invalid data (e.g., negative area)
  - [ ] Saw appropriate error message
  - [ ] Error message is user-friendly
- [ ] Tested form validation:
  - [ ] Left required fields empty
  - [ ] Saw validation errors
  - [ ] Errors cleared when corrected
- [ ] Tested responsive design:
  - [ ] Resized browser window
  - [ ] Layout adapts to mobile size
  - [ ] All features work on mobile

## 📱 Browser Compatibility

Tested in:
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest, if on Mac)

## 🔍 Code Quality Checks

- [ ] No Python errors in backend console
- [ ] No JavaScript errors in browser console
- [ ] All imports resolve correctly
- [ ] No missing dependencies
- [ ] Code follows consistent style

## 📚 Documentation Review

- [ ] Read `README.md`
- [ ] Read `QUICKSTART.md`
- [ ] Reviewed `docs/ML_DESIGN.md`
- [ ] Reviewed `docs/API.md`
- [ ] Reviewed `docs/ARCHITECTURE.md`
- [ ] Understand the project structure

## 🚀 Performance Checks

- [ ] Model training completed in reasonable time (< 5 minutes)
- [ ] Prediction response time < 1 second
- [ ] Frontend loads quickly (< 3 seconds)
- [ ] No memory leaks (checked Task Manager)
- [ ] Backend handles multiple requests

## 🛡️ Security Checks (Production)

For production deployment:
- [ ] Set `DEBUG=False` in backend
- [ ] Use environment variables for sensitive data
- [ ] Configure proper CORS origins
- [ ] Use HTTPS
- [ ] Implement rate limiting
- [ ] Add authentication (if needed)
- [ ] Sanitize user inputs
- [ ] Set up proper logging

## 🎯 Optional Enhancements

- [ ] Set up Git repository: `git init`
- [ ] Create `.gitignore` (already provided)
- [ ] Make initial commit
- [ ] Set up GitHub repository
- [ ] Add more features to the dataset
- [ ] Improve model with hyperparameter tuning
- [ ] Add more visualizations
- [ ] Implement user authentication
- [ ] Add prediction history
- [ ] Deploy to cloud (Heroku, AWS, etc.)

## ❌ Troubleshooting

If you encounter issues, check:

### Model Not Loading
- [ ] Verified model files exist in `ml/models/`
- [ ] Checked file paths in backend config
- [ ] Retrained model if needed

### Backend Won't Start
- [ ] Checked Python version (3.8+)
- [ ] Verified all dependencies installed
- [ ] Checked port 8000 is not in use
- [ ] Reviewed error messages in console

### Frontend Won't Start
- [ ] Checked Node.js version (16+)
- [ ] Deleted `node_modules` and reinstalled
- [ ] Checked port 3000 is not in use
- [ ] Cleared npm cache: `npm cache clean --force`

### CORS Errors
- [ ] Backend is running
- [ ] CORS origins include `http://localhost:3000`
- [ ] Restarted backend after config changes

### Prediction Errors
- [ ] Model is trained and loaded
- [ ] Input data is valid
- [ ] Backend logs show the error
- [ ] Checked API endpoint in frontend

## ✅ Final Verification

- [ ] **ML Pipeline**: Models trained, evaluated, and saved
- [ ] **Backend API**: Running, model loaded, endpoints working
- [ ] **Frontend UI**: Running, form works, predictions display
- [ ] **Integration**: End-to-end flow works perfectly
- [ ] **Documentation**: All docs reviewed and understood

## 🎉 Success Criteria

You're ready to go if:
- ✅ You can make predictions through the UI
- ✅ Predictions are reasonable (not random numbers)
- ✅ Error handling works correctly
- ✅ All three components run without errors
- ✅ You understand how to modify and extend the system

---

**Congratulations!** 🎊 If all items are checked, your House Price Prediction Platform is fully operational!

**Next Steps:**
1. Experiment with different datasets
2. Try improving the model
3. Customize the UI
4. Add new features
5. Deploy to production

**Need Help?** Review the documentation or ask for assistance!
