import React from 'react';
import { NavLink } from 'react-router-dom';

const Header = ({ isLoggedIn, onLogout }) => {
    return (
        <header data-bs-theme="dark">
            <nav className="navbar navbar-expand-lg navbar-dark fixed-top bg-dark">
                <div className="container">
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
                            aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarCollapse">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item">
                                <NavLink className="nav-link" to="/" exact activeclassname="active">
                                    Home
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink className="nav-link" to="/about" activeclassname="active">
                                    About SSH Recipe Recommendation App
                                </NavLink>
                            </li>
                            {/* Show Inventory and Recipes only if logged in */}
                            {isLoggedIn && (
                                <>
                                    <li className="nav-item">
                                        <NavLink className="nav-link" to="/inventory" activeclassname="active">
                                            Inventory
                                        </NavLink>
                                    </li>
                                    <li className="nav-item">
                                        <NavLink className="nav-link" to="/recipes" activeclassname="active">
                                            Recipes
                                        </NavLink>
                                    </li>
                                </>
                            )}
                        </ul>
                        <ul className="navbar-nav ml-auto">
                            {/* Show Login/Register if not logged in */}
                            {!isLoggedIn ? (
                                <>
                                    <li className="nav-item">
                                        <NavLink className="nav-link" to="/login" activeclassname="active">
                                            Login
                                        </NavLink>
                                    </li>
                                    <li className="nav-item">
                                        <NavLink className="nav-link" to="/register" activeclassname="active">
                                            Register
                                        </NavLink>
                                    </li>
                                </>
                            ) : (
                                <>
                                    <li className="nav-item">
                                        <NavLink className="nav-link" to="/preferences" activeclassname="active">
                                            User Preferences
                                        </NavLink>
                                    </li>
                                    <li className="nav-item">
                                        <NavLink
                                            className="nav-link btn"
                                            to="/logout"
                                        >
                                            Log out
                                        </NavLink>
                                    </li>
                                </>
                            )}
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
};

export default Header;
