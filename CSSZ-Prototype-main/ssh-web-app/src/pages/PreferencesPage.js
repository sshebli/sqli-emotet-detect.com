import React, { useState, useEffect } from 'react';


const preferencesList = [
    { id: 1, name: 'Vegetarian', icon: '/styles/images/vegetarian.png' },
    { id: 2, name: 'Vegan', icon: '/styles/images/vegan.png' },
    { id: 3, name: 'Keto', icon: '/styles/images/keto.png' },
    { id: 4, name: 'Gluten Free', icon: '/styles/images/gluten.png' },
    { id: 5, name: 'Dairy free', icon: '/styles/images/dairy.png' },
    { id: 6, name: 'Nut Free', icon: '/styles/images/nut.png' },
    { id: 7, name: 'Shellfish Free', icon: '/styles/images/shellfish.png' },
    { id: 8, name: 'Egg Free', icon: '/styles/images/egg.png' },
    { id: 9, name: 'Soy Free', icon: '/styles/images/soy.png' },
];

const PreferencesPage = ({ userEmail }) => {
  const [selectedPreferences, setSelectedPreferences] = useState([]);
  const [error, setError] = useState('');

  // Fetch user preferences on mount
  useEffect(() => {
    if (!userEmail) {
      setError('User email is missing. Please log in.');
      return;
    }

    fetch(`http://localhost:5001/preferences?email=${userEmail}`)
      .then((response) => {
        if (!response.ok) throw new Error('Error fetching preferences');
        return response.json();
      })
      .then((data) => setSelectedPreferences(data.preferences || []))
      .catch((error) => setError(error.message));
  }, [userEmail]);

  // Toggle preference selection
  const togglePreference = (id) => {
    setSelectedPreferences((prev) =>
      prev.includes(id) ? prev.filter((prefId) => prefId !== id) : [...prev, id]
    );
  };

  // Save preferences to backend
  const savePreferences = () => {
    if (!userEmail) {
      alert('User email is missing. Cannot save preferences.');
      return;
    }

    fetch('http://localhost:5001/preferences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: userEmail, preferences: selectedPreferences }),
    })
      .then((response) => {
        if (!response.ok) throw new Error('Error saving preferences');
        return response.json();
      })
      .then(() => alert('Preferences saved successfully!'))
      .catch((error) => console.error('Error saving preferences:', error));
  };

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="container-fluid mainContainer">
      <h1 className="title_features">User Preferences</h1>
      <p>Select your dietary preferences to help us recommend the best recipes for you:</p>

      <div className="preferences-container">
        {preferencesList.map((preference) => (
          <button
            key={preference.id}
            className={`preference-button ${
              selectedPreferences.includes(preference.id) ? 'selected' : ''
            }`}
            onClick={() => togglePreference(preference.id)}
          >
            <img
              src={preference.icon}
              alt={preference.name}
              className="preference-icon"
            />
            {preference.name}
          </button>
        ))}
      </div>

      <button className="save-button" onClick={savePreferences}>
        Save Preferences
      </button>
    </div>
  );
};

export default PreferencesPage;