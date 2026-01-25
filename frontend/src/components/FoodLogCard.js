const FoodLogCard = ({ foodLog, onDelete, onEdit }) => {
  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <h3>{foodLog.food_name}</h3>
        <div style={styles.actions}>
          {onEdit && (
            <button onClick={() => onEdit(foodLog)} style={styles.editButton}>
              Edit
            </button>
          )}
          {onDelete && (
            <button onClick={() => onDelete(foodLog.id)} style={styles.deleteButton}>
              Delete
            </button>
          )}
        </div>
      </div>
      <div style={styles.content}>
        <p>Calories: {foodLog.calories}</p>
        <p>Protein: {foodLog.protein_g}g</p>
        <p>Carbs: {foodLog.carbs_g}g</p>
        <p>Fats: {foodLog.fats_g}g</p>
        <p>Logged: {new Date(foodLog.logged_at).toLocaleString()}</p>
      </div>
    </div>
  );
};

const styles = {
  card: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '1rem',
    marginBottom: '1rem',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '0.5rem',
  },
  actions: {
    display: 'flex',
    gap: '0.5rem',
  },
  editButton: {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    padding: '0.25rem 0.5rem',
    cursor: 'pointer',
    borderRadius: '4px',
  },
  deleteButton: {
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    padding: '0.25rem 0.5rem',
    cursor: 'pointer',
    borderRadius: '4px',
  },
  content: {
    fontSize: '0.9rem',
  },
};

export default FoodLogCard;
