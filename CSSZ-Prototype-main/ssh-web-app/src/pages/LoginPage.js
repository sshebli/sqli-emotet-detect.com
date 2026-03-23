import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = ({ onLogin }) => {
    const [loginData, setLoginData] = useState({ email: '', password: '' });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLoginData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setErrorMessage('');

        fetch('http://localhost:5001/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Invalid email or password');
                }
                return response.json();
            })
            .then((data) => {
                alert('Login successful!');
                onLogin(data.user.email); // Pass the email to onLogin
                navigate('/welcome');
            })
            .catch((error) => {
                console.error('Error logging in:', error);
                setErrorMessage(error.message || 'Something went wrong. Please try again.');
            })
            .finally(() => {
                setIsSubmitting(false);
            });
    };

    return (
        <div className="container-fluid mainContainer">
            <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
                <h1>Log In</h1>
                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '10px' }}>
                        <label htmlFor="email">Email:</label>
                        <input
                            type="email"
                            name="email"
                            id="email"
                            placeholder="Enter your email"
                            value={loginData.email}
                            onChange={handleChange}
                            required
                            style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
                        />
                    </div>

                    <div style={{ marginBottom: '10px' }}>
                        <label htmlFor="password">Password:</label>
                        <input
                            type="password"
                            name="password"
                            id="password"
                            placeholder="Enter your password"
                            value={loginData.password}
                            onChange={handleChange}
                            required
                            style={{ width: '100%', padding: '8px', marginBottom: '5px' }}
                        />
                    </div>

                    {errorMessage && (
                        <p style={{ color: 'red', fontSize: '0.9em' }}>{errorMessage}</p>
                    )}

                    <button
                        type="submit"
                        disabled={isSubmitting}
                        style={{
                            padding: '10px 20px',
                            backgroundColor: '#4CAF50',
                            color: 'white',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: isSubmitting ? 'not-allowed' : 'pointer',
                        }}
                    >
                        {isSubmitting ? 'Logging in...' : 'Log In'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;
