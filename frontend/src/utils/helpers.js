// Formats a number to Indian Rupee currency format
export const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(value);
};

// Validates all form inputs and returns error messages
export const validateForm = (formData) => {
    const errors = {};

    if (!formData.area || formData.area <= 0) {
        errors.area = 'Enter a valid area';
    } else if (formData.area > 50000) {
        errors.area = 'Area exceeds reasonable limit';
    }

    if (formData.bedrooms === '' || formData.bedrooms < 0) {
        errors.bedrooms = 'Invalid bedroom count';
    } else if (formData.bedrooms > 20) {
        errors.bedrooms = 'Max 20 bedrooms allowed';
    }

    if (formData.bathrooms === '' || formData.bathrooms < 0) {
        errors.bathrooms = 'Invalid bathroom count';
    } else if (formData.bathrooms > 20) {
        errors.bathrooms = 'Max 20 bathrooms allowed';
    }

    if (!formData.location || formData.location.trim() === '') {
        errors.location = 'Location is required';
    }

    if (!formData.state || formData.state.trim() === '') {
        errors.state = 'State is required';
    }

    if (!formData.property_type || formData.property_type.trim() === '') {
        errors.property_type = 'Select property type';
    }

    const currentYear = new Date().getFullYear();
    if (!formData.year_built || formData.year_built < 1800) {
        errors.year_built = 'Year must be 1800 or later';
    } else if (formData.year_built > currentYear + 5) {
        errors.year_built = 'Invalid construction year';
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
};

// Limits the frequency of a function call
export const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
};
