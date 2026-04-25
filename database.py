import mysql.connector
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1919',
    'database': 'disk_analyzer'
}

def init_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("USE disk_analyzer")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME,
                cpu_usage FLOAT,
                ram_usage FLOAT,
                disk_usage FLOAT,
                read_speed FLOAT,
                write_speed FLOAT,
                health_status VARCHAR(20),
                best_algorithm VARCHAR(20),
                fcfs_seeks INT,
                sstf_seeks INT,
                scan_seeks INT,
                cscan_seeks INT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False

def save_result(metrics, health_status, scheduler_results, best_algorithm):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_results 
            (timestamp, cpu_usage, ram_usage, disk_usage, read_speed, write_speed,
             health_status, best_algorithm, fcfs_seeks, sstf_seeks, scan_seeks, cscan_seeks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            datetime.now(),
            metrics['cpu'],
            metrics['ram'],
            metrics['disk'],
            metrics['read_speed'],
            metrics['write_speed'],
            health_status,
            best_algorithm,
            scheduler_results['FCFS']['total'],
            scheduler_results['SSTF']['total'],
            scheduler_results['SCAN']['total'],
            scheduler_results['C-SCAN']['total']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Save error: {e}")
        return False

def get_history(limit=10):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM analysis_results ORDER BY timestamp DESC LIMIT {limit}")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except mysql.connector.Error as e:
        print(f"Fetch error: {e}")
        return []