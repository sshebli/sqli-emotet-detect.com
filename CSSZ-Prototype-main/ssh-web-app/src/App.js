import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ClerkProvider } from '@clerk/clerk-react';


import Header from './components/Header';
import Footer from './components/Footer';

import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import RegistrationPage from './pages/RegistrationPage';

import LoginPage from './pages/LoginPage';
import LogoutPage from './pages/LogoutPage';

import InventoryPage from './pages/InventoryPage';
import RecipesPage from './pages/RecipesPage';
import PreferencesPage from './pages/PreferencesPage';

import WelcomePage from './pages/WelcomePage';
import FaqPage from './pages/FaqPage';
import PrivacyPolicyPage from './pages/PrivacyPolicyPage';

const clerkPubKey = process.env.REACT_APP_CLERK_PUBLISHABLE_KEY

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState(null);

  const handleLogin = (email) => {
    setIsLoggedIn(true);
    setUserEmail(email);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserEmail(null);
  };

  return (
    <ClerkProvider publishableKey={clerkPubKey}>
      <Router>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          {/* Header */}
          <Header isLoggedIn={isLoggedIn} onLogout={handleLogout} />

          {/* Main Content */}
          <div style={{ flex: '1' }}>
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<HomePage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/login" element={<LoginPage onLogin={(email) => handleLogin(email)} />} />
              <Route path="/register" element={<RegistrationPage onLogin={(email) => handleLogin(email)} />} />

              <Route path="/welcome" element={<WelcomePage />} />
              <Route path="/logout" element={<LogoutPage onLogout={handleLogout} />} />
              <Route path="/faq" element={<FaqPage />} />
              <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />

              {/* Private Routes */}
              {isLoggedIn && (
                <>
                  <Route path="/inventory" element={<InventoryPage />} />
                  <Route path="/recipes" element={<RecipesPage />} />
                  <Route
                    path="/preferences"
                    element={<PreferencesPage userEmail={userEmail} />}
                  />
                </>
              )}
            </Routes>
          </div>

          {/* Footer */}
          <Footer isLoggedIn={isLoggedIn} />
        </div>
      </Router>
    </ClerkProvider>
  );
};


export default App;
