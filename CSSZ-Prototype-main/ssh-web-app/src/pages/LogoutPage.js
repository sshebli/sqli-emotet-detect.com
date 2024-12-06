import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutPage = ({ onLogout }) => {
    const navigate = useNavigate();

    const handleConfirmLogout = () => {
        alert('Log out successful');
        onLogout(); // Reset login state
        navigate('/');
    };

    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
            }}
        >
            <h1 className="subHeading_style">Are you sure you want to log out?</h1>
            <button
                onClick={handleConfirmLogout}
                style={{
                    padding: '10px 20px',
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    fontSize: '16px',
                    marginTop: '20px',
                }}
            >
                Log out
            </button>
        </div>
    );
};

export default LogoutPage;
