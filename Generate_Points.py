import mysql.connector
import numpy as np

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Urs5658?!",
    database="points_db"
)
cursor = db.cursor()

# Create table (if not exists)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS points (
        id INT AUTO_INCREMENT PRIMARY KEY,
        x DOUBLE NOT NULL,
        y DOUBLE NOT NULL
    )
""")

# Generate 100 million random points (batches of 1 million)
total_points = 100_000_000
batch_size = 1_000_000

for _ in range(total_points // batch_size):
    # Generate batch of points
    x_coords = np.random.uniform(0, 1000, batch_size).tolist()
    y_coords = np.random.uniform(0, 1000, batch_size).tolist()
    
    # Bulk insert
    values = list(zip(x_coords, y_coords))
    cursor.executemany("INSERT INTO points (x, y) VALUES (%s, %s)", values)
    db.commit()
    print(f"Inserted {cursor.rowcount} points")

cursor.close()
db.close()