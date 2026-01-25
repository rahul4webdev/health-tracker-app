import { useState, useEffect } from 'react';
import { getFoodLogs, createFoodLog, deleteFoodLog } from '../services/nutritionService';
import FoodLogCard from '../components/FoodLogCard';

const FoodLogPage = () => {
  const [foodLogs, setFoodLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    food_name: '',
    calories: '',
    protein_g: '',
    carbs_g: '',
    fats_g: '',
    logged_at: new Date().toISOString().slice(0, 16),
  });

  useEffect(() => {
    fetchFoodLogs();
  }, []);

  const fetchFoodLogs = async () => {
    try {
      const data = await getFoodLogs();
      setFoodLogs(data);
    } catch (error) {
      console.error('Failed to fetch food logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createFoodLog(formData);
      setShowForm(false);
      fetchFoodLogs();
      setFormData({
        food_name: '',
        calories: '',
        protein_g: '',
        carbs_g: '',
        fats_g: '',
        logged_at: new Date().toISOString().slice(0, 16),
      });
    } catch (error) {
      alert('Failed to create food log');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this entry?')) {
      try {
        await deleteFoodLog(id);
        fetchFoodLogs();
      } catch (error) {
        alert('Failed to delete food log');
      }
    }
  };

  if (loading) return <div style={styles.container}>Loading...</div>;

  return (
    <div style={styles.container}>
      <h1>Food Log</h1>
      <button onClick={() => setShowForm(!showForm)} style={styles.addButton}>
        {showForm ? 'Cancel' : 'Add Entry'}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="text"
            placeholder="Food Name"
            value={formData.food_name}
            onChange={(e) => setFormData({ ...formData, food_name: e.target.value })}
            required
            style={styles.input}
          />
          <input
            type="number"
            step="0.01"
            placeholder="Calories"
            value={formData.calories}
            onChange={(e) => setFormData({ ...formData, calories: e.target.value })}
            required
            style={styles.input}
          />
          <input
            type="number"
            step="0.01"
            placeholder="Protein (g)"
            value={formData.protein_g}
            onChange={(e) => setFormData({ ...formData, protein_g: e.target.value })}
            style={styles.input}
          />
          <input
            type="number"
            step="0.01"
            placeholder="Carbs (g)"
            value={formData.carbs_g}
            onChange={(e) => setFormData({ ...formData, carbs_g: e.target.value })}
            style={styles.input}
          />
          <input
            type="number"
            step="0.01"
            placeholder="Fats (g)"
            value={formData.fats_g}
            onChange={(e) => setFormData({ ...formData, fats_g: e.target.value })}
            style={styles.input}
          />
          <input
            type="datetime-local"
            value={formData.logged_at}
            onChange={(e) => setFormData({ ...formData, logged_at: e.target.value })}
            required
            style={styles.input}
          />
          <button type="submit" style={styles.submitButton}>
            Add Entry
          </button>
        </form>
      )}

      <div style={styles.logs}>
        {foodLogs.map((log) => (
          <FoodLogCard key={log.id} foodLog={log} onDelete={handleDelete} />
        ))}
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
  addButton: {
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    padding: '0.75rem 1.5rem',
    cursor: 'pointer',
    borderRadius: '4px',
    marginBottom: '1rem',
  },
  form: {
    backgroundColor: 'white',
    padding: '1.5rem',
    borderRadius: '8px',
    marginBottom: '1rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  input: {
    width: '100%',
    padding: '0.5rem',
    marginBottom: '0.5rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
  },
  submitButton: {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    padding: '0.75rem 1.5rem',
    cursor: 'pointer',
    borderRadius: '4px',
  },
  logs: {
    marginTop: '1rem',
  },
};

export default FoodLogPage;
