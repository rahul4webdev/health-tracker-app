import { useState, useEffect } from 'react';
import { getDailySummary } from '../services/nutritionService';

const DashboardPage = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const data = await getDailySummary(today);
      setSummary(data);
    } catch (error) {
      console.error('Failed to fetch summary:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={styles.container}>Loading...</div>;

  return (
    <div style={styles.container}>
      <h1>Dashboard</h1>
      <div style={styles.card}>
        <h2>Today's Nutrition Summary</h2>
        {summary && (
          <div style={styles.summary}>
            <div style={styles.stat}>
              <span style={styles.label}>Calories:</span>
              <span style={styles.value}>{summary.total_calories}</span>
            </div>
            <div style={styles.stat}>
              <span style={styles.label}>Protein:</span>
              <span style={styles.value}>{summary.total_protein_g}g</span>
            </div>
            <div style={styles.stat}>
              <span style={styles.label}>Carbs:</span>
              <span style={styles.value}>{summary.total_carbs_g}g</span>
            </div>
            <div style={styles.stat}>
              <span style={styles.label}>Fats:</span>
              <span style={styles.value}>{summary.total_fats_g}g</span>
            </div>
            <div style={styles.stat}>
              <span style={styles.label}>Entries:</span>
              <span style={styles.value}>{summary.entries_count}</span>
            </div>
          </div>
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
  summary: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  stat: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0.5rem 0',
    borderBottom: '1px solid #eee',
  },
  label: {
    fontWeight: 'bold',
  },
  value: {
    fontSize: '1.2rem',
  },
};

export default DashboardPage;
