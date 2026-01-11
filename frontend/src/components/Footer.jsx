import React from 'react';
import './Footer.css';

// Site footer with project details and attribution
const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="app-footer">
            <div className="footer-content">
                <div className="footer-section">
                    <h3>About</h3>
                    <p>
                        AI-powered house price prediction using advanced machine learning algorithms.
                        Built with production-grade engineering practices.
                    </p>
                </div>

                <div className="footer-section">
                    <h3>Technology</h3>
                    <ul>
                        <li>React Frontend</li>
                        <li>FastAPI Backend</li>
                        <li>Scikit-learn ML</li>
                        <li>Random Forest</li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h3>Features</h3>
                    <ul>
                        <li>Real-time Predictions</li>
                        <li>All-India Coverage</li>
                        <li>Confidence Intervals</li>
                        <li>Responsive Design</li>
                    </ul>
                </div>
            </div>

            <div className="footer-bottom">
                <p>&copy; {currentYear} House Price Predictor | <strong>DEVELOPED BY AYUSH</strong></p>
            </div>
        </footer>
    );
};

export default Footer;
