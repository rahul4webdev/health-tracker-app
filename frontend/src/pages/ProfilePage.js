import { useState, useEffect } from 'react';
import { getProfile, updateProfile } from '../services/profileService';

const ProfilePage = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await getProfile();
      setProfile(data);
      setFormData(data);
    } catch (error) {
      console.error('Failed to fetch profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const updated = await updateProfile(formData);
      setProfile(updated);
      setEditing(false);
    } catch (error) {
      alert('Failed to update profile');
    }
  };

  if (loading) return <div style={styles.container}>Loading...</div>;

  return (
    <div style={styles.container}>
      <h1>Profile</h1>
      <div style={styles.card}>
        {!editing ? (
          <div>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Name:</strong> {profile.name || 'Not set'}</p>
            <p><strong>Age:</strong> {profile.age || 'Not set'}</p>
            <p><strong>Gender:</strong> {profile.gender || 'Not set'}</p>
            <p><strong>Height:</strong> {profile.height_cm ? `${profile.height_cm} cm` : 'Not set'}</p>
            <p><strong>Weight:</strong> {profile.weight_kg ? `${profile.weight_kg} kg` : 'Not set'}</p>
            <p><strong>Activity Level:</strong> {profile.activity_level || 'Not set'}</p>
            <button onClick={() => setEditing(true)} style={styles.button}>
              Edit Profile
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div style={styles.formGroup}>
              <label>Name:</label>
              <input
                type="text"
                value={formData.name || ''}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                style={styles.input}
              />
            </div>
            <div style={styles.formGroup}>
              <label>Age:</label>
              <input
                type="number"
                value={formData.age || ''}
                onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                style={styles.input}
              />
            </div>
            <div style={styles.formGroup}>
              <label>Gender:</label>
              <select
                value={formData.gender || ''}
                onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                style={styles.input}
              >
                <option value="">Select...</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div style={styles.formGroup}>
              <label>Height (cm):</label>
              <input
                type="number"
                step="0.01"
                value={formData.height_cm || ''}
                onChange={(e) => setFormData({ ...formData, height_cm: e.target.value })}
                style={styles.input}
              />
            </div>
            <div style={styles.formGroup}>
              <label>Weight (kg):</label>
              <input
                type="number"
                step="0.01"
                value={formData.weight_kg || ''}
                onChange={(e) => setFormData({ ...formData, weight_kg: e.target.value })}
                style={styles.input}
              />
            </div>
            <div style={styles.formGroup}>
              <label>Activity Level:</label>
              <select
                value={formData.activity_level || ''}
                onChange={(e) => setFormData({ ...formData, activity_level: e.target.value })}
                style={styles.input}
              >
                <option value="">Select...</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <button type="submit" style={styles.button}>
              Save
            </button>
            <button type="button" onClick={() => setEditing(false)} style={styles.cancelButton}>
              Cancel
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem',
  },
  card: {
    backgroundColor: 'white',
    padding: '2rem',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  formGroup: {
    marginBottom: '1rem',
  },
  input: {
    width: '100%',
    padding: '0.5rem',
    marginTop: '0.25rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
  },
  button: {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    padding: '0.75rem 1.5rem',
    cursor: 'pointer',
    borderRadius: '4px',
    marginRight: '0.5rem',
  },
  cancelButton: {
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    padding: '0.75rem 1.5rem',
    cursor: 'pointer',
    borderRadius: '4px',
  },
};

export default ProfilePage;
