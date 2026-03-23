import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebookF, faTwitter, faYoutube, faLinkedin, faInstagram } from '@fortawesome/free-brands-svg-icons';
import { Link, useNavigate } from 'react-router-dom';

const Footer = ({ isLoggedIn }) => {
    const navigate = useNavigate();

    const handleNavigation = (path) => {
        if (isLoggedIn) {
            navigate(path); // Navigate to the intended page
        } else {
            navigate('/login'); // Redirect to login if not logged in
        }
    };

    return (
        <footer className="container">
            <div className="row footerRow">
                <div className="col-lg-4 col-sm-12" style={{ maxWidth: '315px' }}>
                    <img src="/styles/images/logo.png" alt="SSH Homes" style={{ width: '250px', height: '71px' }} />
                </div>
                <div className="col-lg-3 col-sm-3">
                    <ul>
                        <div>
                            <Link to="/about" className="footerTextStyle" style={{ textDecoration: 'none' }}>
                                About SSH Homes Recipe Recommendation App
                            </Link>
                            <p></p>
                        </div>
                        <div>
                            <p
                                className="footerTextStyle"
                                onClick={() => handleNavigation('/recipes')}
                                style={{ cursor: 'pointer'}}
                            >
                                Recipes
                            </p>
                        </div>
                        <div>
                            <p
                                className="footerTextStyle"
                                onClick={() => handleNavigation('/inventory')}
                                style={{ cursor: 'pointer'}}
                            >
                                Inventory
                            </p>
                        </div>
                        <div>
                            <p
                                className="footerTextStyle"
                                onClick={() => handleNavigation('/preferences')}
                                style={{ cursor: 'pointer'}}
                            >
                                Preferences
                            </p>
                        </div>
                    </ul>
                </div>
                <div className="col-lg-2 col-sm-2">
                    <ul>
                        <div>
                            <Link to="/login" className="footerTextStyle" style={{ textDecoration: 'none' }}>
                                Login
                            </Link>
                            <p></p>
                        </div>
                        <div>
                            <Link to="/register" className="footerTextStyle" style={{ textDecoration: 'none' }}>
                                Register
                            </Link>
                            <p></p>
                        </div>
                        <div>
                            <Link to="/faq" className="footerTextStyle" style={{ textDecoration: 'none' }}>
                                FAQ
                            </Link>
                            <p></p>
                        </div>
                        <div>
                            <Link to="/privacy-policy" className="footerTextStyle" style={{ textDecoration: 'none' }}>
                                Privacy Policy
                            </Link>
                            <p></p>
                        </div>
                    </ul>
                </div>
                <div className="col-lg-3 col-sm-3">
                    <ul>
                        <div>
                            <p className="footerTextStyle locationIcon">
                                University of Birmingham - Dubai - United Arab Emirates
                            </p>
                        </div>
                        <div>
                            <p className="footerTextStyle phoneIcon">+123 345123 556</p>
                        </div>
                        <div>
                            <p className="footerTextStyle emailIcon">support@shhhomes.com</p>
                        </div>
                        <div>
                            <p className="footerTextStyle">Website last update: December 4, 2024</p>
                        </div>
                    </ul>
                </div>
            </div>

            <div className="row">
                <div className="col-md-8">
                    <div style={{ marginTop: '10px' }}>
                        <p className="footerTextStyle socials" style={{ color: '#282828', position: 'relative', left: '0px' }}>
                            © 2024 SSH Smart Home Systems
                        </p>
                    </div>
                </div>
                <div className="col-md-2 icons">
                    <FontAwesomeIcon icon={faFacebookF} style={{ color: '#797979', marginRight: '10px' }} />
                    <FontAwesomeIcon icon={faTwitter} style={{ color: '#797979', marginRight: '10px' }} />
                    <FontAwesomeIcon icon={faYoutube} style={{ color: '#797979', marginRight: '10px' }} />
                    <FontAwesomeIcon icon={faLinkedin} style={{ color: '#797979', marginRight: '10px' }} />
                    <FontAwesomeIcon icon={faInstagram} style={{ color: '#797979' }} />
                </div>
            </div>
        </footer>
    );
};

export default Footer;
