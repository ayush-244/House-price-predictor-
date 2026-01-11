import React from 'react';
import './Header.css';

// Main navigation and logo header
const Header = () => {
    return (
        <header className="app-header">
            <div className="header-content">
                <div className="logo">
                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                        <rect width="40" height="40" rx="12" fill="url(#headerGradient)" />
                        <path d="M20 10L12 16V28H16V22H24V28H28V16L20 10Z" fill="white" />
                        <defs>
                            <linearGradient id="headerGradient" x1="0" y1="0" x2="40" y2="40">
                                <stop offset="0%" stopColor="#667eea" />
                                <stop offset="100%" stopColor="#764ba2" />
                            </linearGradient>
                        </defs>
                    </svg>
                    <div className="logo-text">
                        <h1>House Price Predictor</h1>
                        <span>AI-Powered Valuation</span>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
