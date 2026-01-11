import React, { useState, useEffect } from 'react';
import { predictPrice, getOptions } from '../services/api';
import { validateForm, formatCurrency } from '../utils/helpers';
import './PredictionForm.css';

const PredictionForm = () => {
    // Stores all form input values
    const [formData, setFormData] = useState({
        area: '',
        bedrooms: '',
        bathrooms: '',
        location: '',
        year_built: '',
        state: '',
        property_type: '',
        parking: '0',
        modular_kitchen: '0',
        dining_hall: '0'
    });

    // Dropdown data fetched from API
    const [locationsMap, setLocationsMap] = useState({});
    const [propertyTypeList, setPropertyTypeList] = useState([]);

    // UI and application state
    const [loading, setLoading] = useState(false);
    const [prediction, setPrediction] = useState(null);
    const [errors, setErrors] = useState({});
    const [apiError, setApiError] = useState('');

    // Fetch dynamic options (states/cities) when component loads
    useEffect(() => {
        const loadOptions = async () => {
            const data = await getOptions();
            if (data) {
                setLocationsMap(data.locations || {});
                if (data.property_types && data.property_types.length > 0) {
                    setPropertyTypeList(data.property_types);
                }
            }
        };
        loadOptions();
    }, []);

    // Helpers to filter cities based on selected state
    const states = Object.keys(locationsMap).sort();
    const availableCities = formData.state ? (locationsMap[formData.state] || []) : [];

    // Sync input changes with local state
    const handleChange = (e) => {
        const { name, value } = e.target;

        setFormData(prev => {
            const newData = { ...prev, [name]: value };
            if (name === 'state') newData.location = '';
            return newData;
        });

        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    // Submits data to the backend for price evaluation
    const handleSubmit = async (e) => {
        e.preventDefault();
        setPrediction(null);
        setApiError('');

        const processedData = {
            area: parseFloat(formData.area),
            bedrooms: parseInt(formData.bedrooms),
            bathrooms: parseFloat(formData.bathrooms),
            location: formData.location.trim(),
            year_built: parseInt(formData.year_built),
            state: formData.state.trim(),
            property_type: formData.property_type.trim(),
            parking: parseInt(formData.parking),
            modular_kitchen: parseInt(formData.modular_kitchen),
            dining_hall: parseInt(formData.dining_hall)
        };

        const validation = validateForm(processedData);
        if (!validation.isValid) {
            setErrors(validation.errors);
            return;
        }

        setLoading(true);
        try {
            const result = await predictPrice(processedData);
            setPrediction(result);
            setErrors({});
        } catch (error) {
            setApiError(error.message);
        } finally {
            setLoading(false);
        }
    };

    // Clears all inputs and results
    const handleReset = () => {
        setFormData({
            area: '', bedrooms: '', bathrooms: '', location: '',
            year_built: '', state: '', property_type: '', parking: '0',
            modular_kitchen: '0', dining_hall: '0'
        });
        setPrediction(null);
        setErrors({});
        setApiError('');
    };

    return (
        <div className="prediction-form-container">
            <div className="form-header" style={{ animationDelay: '0.1s' }}>
                <h2>Predict House Price</h2>
                <p>Enter property details for an AI-powered estimate</p>
            </div>

            <form onSubmit={handleSubmit} className="prediction-form">
                <div className="form-group" style={{ animationDelay: '0.2s' }}>
                    <label htmlFor="area">Living Area (sqft) <span className="required">*</span></label>
                    <input
                        type="number" id="area" name="area" value={formData.area}
                        onChange={handleChange} placeholder="e.g., 2500"
                        className={errors.area ? 'error' : ''} step="0.01"
                    />
                    {errors.area && <span className="error-message">{errors.area}</span>}
                </div>

                <div className="form-row" style={{ animationDelay: '0.3s' }}>
                    <div className="form-group">
                        <label htmlFor="bedrooms">Bedrooms <span className="required">*</span></label>
                        <input
                            type="number" id="bedrooms" name="bedrooms" value={formData.bedrooms}
                            onChange={handleChange} placeholder="e.g., 3"
                            className={errors.bedrooms ? 'error' : ''} min="0" step="1"
                        />
                        {errors.bedrooms && <span className="error-message">{errors.bedrooms}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="bathrooms">Bathrooms <span className="required">*</span></label>
                        <input
                            type="number" id="bathrooms" name="bathrooms" value={formData.bathrooms}
                            onChange={handleChange} placeholder="e.g., 2.5"
                            className={errors.bathrooms ? 'error' : ''} min="0" step="0.5"
                        />
                        {errors.bathrooms && <span className="error-message">{errors.bathrooms}</span>}
                    </div>
                </div>

                <div className="form-group" style={{ animationDelay: '0.4s' }}>
                    <label htmlFor="state">State <span className="required">*</span></label>
                    <select id="state" name="state" value={formData.state} onChange={handleChange} className={errors.state ? 'error' : ''}>
                        <option value="">Select State</option>
                        {states.map(state => <option key={state} value={state}>{state}</option>)}
                    </select>
                    {errors.state && <span className="error-message">{errors.state}</span>}
                </div>

                <div className="form-group" style={{ animationDelay: '0.5s' }}>
                    <label htmlFor="location">Location (City) <span className="required">*</span></label>
                    <select id="location" name="location" value={formData.location} onChange={handleChange} className={errors.location ? 'error' : ''} disabled={!formData.state}>
                        <option value="">{formData.state ? "Select City" : "Select State First"}</option>
                        {availableCities.map(city => <option key={city} value={city}>{city}</option>)}
                    </select>
                    {errors.location && <span className="error-message">{errors.location}</span>}
                </div>

                <div className="form-row" style={{ animationDelay: '0.6s' }}>
                    <div className="form-group">
                        <label htmlFor="property_type">Property Type <span className="required">*</span></label>
                        <select id="property_type" name="property_type" value={formData.property_type} onChange={handleChange} className={errors.property_type ? 'error' : ''}>
                            <option value="">Select Type</option>
                            {propertyTypeList.map(type => <option key={type} value={type}>{type}</option>)}
                        </select>
                        {errors.property_type && <span className="error-message">{errors.property_type}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="parking">Parking <span className="required">*</span></label>
                        <select id="parking" name="parking" value={formData.parking} onChange={handleChange}>
                            <option value="0">No</option>
                            <option value="1">Yes</option>
                        </select>
                    </div>
                </div>

                <div className="form-row" style={{ animationDelay: '0.7s' }}>
                    <div className="form-group">
                        <label htmlFor="modular_kitchen">Modular Kitchen</label>
                        <select id="modular_kitchen" name="modular_kitchen" value={formData.modular_kitchen} onChange={handleChange}>
                            <option value="0">No</option>
                            <option value="1">Yes</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="dining_hall">Dining Hall</label>
                        <select id="dining_hall" name="dining_hall" value={formData.dining_hall} onChange={handleChange}>
                            <option value="0">No</option>
                            <option value="1">Yes</option>
                        </select>
                    </div>
                </div>

                <div className="form-group" style={{ animationDelay: '0.8s' }}>
                    <label htmlFor="year_built">Year Built <span className="required">*</span></label>
                    <input
                        type="number" id="year_built" name="year_built" value={formData.year_built}
                        onChange={handleChange} placeholder="e.g., 2010"
                        className={errors.year_built ? 'error' : ''} min="1800"
                    />
                    {errors.year_built && <span className="error-message">{errors.year_built}</span>}
                </div>

                {apiError && (
                    <div className="api-error">
                        <span>{apiError}</span>
                    </div>
                )}

                <div className="form-actions">
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        {loading ? "Predicting..." : "Get Prediction"}
                    </button>
                    <button type="button" className="btn btn-secondary" onClick={handleReset} disabled={loading}>
                        Reset
                    </button>
                </div>
            </form>

            {prediction && (
                <div className="prediction-result">
                    <div className="result-header">
                        <h3>Prediction Complete!</h3>
                    </div>
                    <div className="result-price">
                        <span className="price-label">Estimated Price</span>
                        <span className="price-value">{formatCurrency(prediction.predicted_price)}</span>
                    </div>
                    {prediction.confidence_interval && (
                        <div className="confidence-interval">
                            <span className="interval-label">Confidence Range</span>
                            <div className="interval-range">
                                {formatCurrency(prediction.confidence_interval.lower)} — {formatCurrency(prediction.confidence_interval.upper)}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default PredictionForm;
