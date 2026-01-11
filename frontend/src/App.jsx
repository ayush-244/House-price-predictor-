import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import PredictionForm from './components/PredictionForm';
import './App.css';

// Root component for the main application layout
function App() {
    return (
        <div className="app">
            <Header />

            <main className="main-content">
                <div className="hero-section">
                    <h2 className="hero-title">Predict Your House Value</h2>
                    <p className="hero-subtitle">
                        Get instant, AI-powered price estimates using advanced machine learning models
                        trained on real-world housing data.
                    </p>
                </div>

                <PredictionForm />

                <div className="features-section">
                    <h3>Why Choose Our Platform?</h3>
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="feature-icon">
                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                    <circle cx="16" cy="16" r="16" fill="url(#grad1)" />
                                    <path d="M16 8L20 12L16 16L12 12L16 8Z" fill="white" />
                                    <path d="M16 16L20 20L16 24L12 20L16 16Z" fill="white" opacity="0.7" />
                                    <defs>
                                        <linearGradient id="grad1" x1="0" y1="0" x2="32" y2="32">
                                            <stop offset="0%" stopColor="#667eea" />
                                            <stop offset="100%" stopColor="#764ba2" />
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <h4>Advanced ML Models</h4>
                            <p>Powered by Random Forest Regressor trained on 300,000+ real estate records.</p>
                        </div>

                        <div className="feature-card">
                            <div className="feature-icon">
                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                    <circle cx="16" cy="16" r="16" fill="url(#grad2)" />
                                    <path d="M10 16L14 20L22 12" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                                    <defs>
                                        <linearGradient id="grad2" x1="0" y1="0" x2="32" y2="32">
                                            <stop offset="0%" stopColor="#f093fb" />
                                            <stop offset="100%" stopColor="#f5576c" />
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <h4>Pro Accuracy</h4>
                            <p>High-fidelity predictions with R² &gt; 0.90 reliability score.</p>
                        </div>

                        <div className="feature-card">
                            <div className="feature-icon">
                                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                    <circle cx="16" cy="16" r="16" fill="url(#grad3)" />
                                    <path d="M16 10V22M10 16H22" stroke="white" strokeWidth="2.5" strokeLinecap="round" />
                                    <defs>
                                        <linearGradient id="grad3" x1="0" y1="0" x2="32" y2="32">
                                            <stop offset="0%" stopColor="#4facfe" />
                                            <stop offset="100%" stopColor="#00f2fe" />
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <h4>Instant Results</h4>
                            <p>Get predictions in milliseconds with confidence intervals</p>
                        </div>
                    </div>
                </div>
            </main>

            <Footer />

            <div className="dev-badge">
                <span className="dev-badge-dot"></span>
                Developed by Ayush
            </div>
        </div>
    );
}

export default App;
