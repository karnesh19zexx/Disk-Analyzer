# Disk-Analyzer

# ML-Based Disk I/O Performance Analysis for LINUX / Windows

A comprehensive web application that analyzes disk I/O performance using system metrics, database queries, algorithms, and machine learning predictions.

//Note : windows users can run the code file via vs code or appropriate CMD command

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Technical Details](#technical-details)
  - [Operating Systems Module](#operating-systems-module)
  - [DBMS Module](#dbms-module)
  - [DAA Module](#daa-module)
  - [Machine Learning Module](#machine-learning-module)
- [API Endpoints](#api-endpoints)
- [Subject Connections](#subject-connections)

---

## Overview

This project combines concepts from:

1. **Operating Systems (OS)** - Disk scheduling, process scheduling, CPU I/O wait
2. **DBMS** - Query execution time, indexing effects, buffer management
3. **DAA (Design & Analysis of Algorithms)** - Searching algorithms, time complexity
4. **Machine Learning** - Classification, prediction models

The web app collects real-time system metrics, stores them in a database, runs algorithm comparisons, and uses ML to predict system performance.

---

## Features

### 1. Real-time System Monitoring

- CPU usage percentage
- Memory usage percentage
- Disk I/O read/write speeds
- Disk usage percentage
- I/O count (read/write operations)

### 2. Disk Scheduling Algorithms (OS)

- **FCFS** (First-Come-First-Served)
- **SSTF** (Shortest Seek Time First)
- **SCAN** (Elevator algorithm)
- **C-SCAN** (Circular SCAN)

### 3. Search Algorithm Comparison (DAA)

- Linear Search vs Binary Search
- Visual comparison of time complexity

### 4. DBMS Query Benchmark

- Query execution time simulation
- Index vs non-index comparison

### 5. ML Performance Prediction

- Random Forest classifier
- Predicts: Good, Medium, or Poor performance

---

## Project Structure

```
disk-io-analysis/
├── app.py              # Main Flask application
├── metrics.py          # OS metrics collection (psutil)
├── algorithms.py       # Disk scheduling & search algorithms
├── ml_model.py        # ML prediction model
├── models.py         # Database models (SQLAlchemy)
├── requirements.txt  # Python dependencies
├── templates/
│   └── index.html  # Web UI with Chart.js
├── venv/           # Virtual environment
└── disk_io.db      # SQLite database (auto-created)
```

---

## Installation

### Prerequisites

- Python 3.8+
- MySQL (optional - uses SQLite by default)

### Setup

1. **Create project directory:**

   ```bash
   mkdir -p ~/Projects/disk-io-analysis
   cd ~/Projects/disk-io-analysis
   ```

2. **Create virtual environment:**

   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment:**

   ```bash
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate  # Windows
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:

   ```bash
   pip install flask flask_sqlalchemy psutil pandas numpy scikit-learn joblib
   ```

---

## How to Run

### Start the Web Application

```bash
cd ~/Projects/disk-io-analysis
source venv/bin/activate
python app.py
```

### Access the Web UI

Open your browser and navigate to:

```
http://localhost:5000
```

### Using the Application

1. **View Live Metrics** - Dashboard shows real-time CPU, memory, disk usage
2. **Disk Scheduling** - Click "Run Comparison" to compare FCFS/SSTF/SCAN/C-SCAN
3. **Search Algorithms** - Enter data size and click "Compare Search"
4. **DBMS Query** - Click "With Index" or "Without Index" to test query performance
5. **ML Prediction** - Click "Predict Current" for ML-based performance prediction

---

## Technical Details

### Operating Systems Module (`metrics.py`)

Uses **psutil** library to collect system metrics:

```python
import psutil

class MetricsCollector:
    def collect(self):
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        disk_io = psutil.disk_io_counters()
        # Returns: {cpu_percent, memory_percent, disk_usage, ...}
```

**OS Concepts Covered:**

- CPU I/O wait time
- Disk response time
- Process scheduling delay
- Virtual memory usage
- File system performance

### DBMS Module

Query benchmark simulates database operations:

```python
# With indexing (faster)
if has_index:
    time.sleep(0.001 * (size / 100))

# Without indexing (slower)
else:
    time.sleep(0.01 * (size / 100))
```

**DBMS Concepts Covered:**

- Query execution time
- Indexing effects on disk I/O
- Buffer management simulation
- Transaction delay

### DAA Module (`algorithms.py`)

#### Disk Scheduling Algorithms:

```python
class DiskScheduler:
    def fcfs(self):       # First-Come-First-Served
    def sstf(self):     # Shortest Seek Time First
    def scan(self):       # SCAN (Elevator)
    def cscan(self):     # C-SCAN (Circular)
```

#### Search Algorithms:

```python
class SearchAlgorithms:
    @staticmethod
    def linear_search(arr, target):  # O(n) - Linear
    @staticmethod
    def binary_search(arr, target):  # O(log n) - Binary
```

### Machine Learning Module (`ml_model.py`)

Uses **scikit-learn** Random Forest classifier:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class MLModel:
    def _generate_synthetic_data(self):
        # Generate training data based on system thresholds
    
    def _train_model(self):
        # Train Random Forest classifier
    
    def predict(self, features):
        # Predict: Good, Medium, or Poor
```

**ML Features Used:**

- cpu_percent
- memory_percent
- disk_usage
- io_count_read
- io_count_write
- disk_read_bytes
- disk_write_bytes

---

## API Endpoints

| Endpoint               | Method | Description                    |
| ---------------------- | ------ | ------------------------------ |
| `/`                    | GET    | Main dashboard                 |
| `/api/metrics`         | GET    | Current system metrics         |
| `/api/metrics/history` | GET    | Historical metrics             |
| `/api/disk-schedule`   | POST   | Run disk scheduling comparison |
| `/api/search-compare`  | POST   | Compare search algorithms      |
| `/api/query-benchmark` | POST   | DBMS query benchmark           |
| `/api/predict`         | POST   | ML prediction                  |
| `/api/predict/current` | GET    | Predict current performance    |

### Example API Calls

```bash
# Get current metrics
curl http://localhost:5000/api/metrics

# Run disk scheduling
curl -X POST http://localhost:5000/api/disk-schedule \
  -H "Content-Type: application/json" \
  -d '{"requests": [10, 22, 5, 45, 30], "initial_head": 50}'

# Run ML prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"cpu_percent": 50, "memory_percent": 60, "disk_usage": 70}'
```

---

## Subject Connections

### 1. Operating Systems

- **Disk Scheduling**: FCFS, SSTF, SCAN, C-SCAN algorithms
- **Process Scheduling**: CPU usage monitoring
- **CPU I/O Wait**: Performance class calculation
- **File System Performance**: Disk usage and I/O statistics

### 2. DBMS

- **Query Execution Time**: Simulated query benchmarks
- **Indexing Effect**: Compare with/without index
- **Buffer Management**: Query log storage
- **Disk Access**: I/O operation counts

### 3. DAA

- **Time Complexity**: O(n) vs O(log n)
- **Searching Algorithms**: Linear vs Binary search
- **Scheduling Optimization**: Disk arm movement calculation
- **Greedy Algorithm**: SSTF uses greedy approach

### 4. Machine Learning

- **Data Collection**: System metrics as features
- **Feature Selection**: 7 key metrics
- **Classification**: Random Forest (Good/Medium/Poor)
- **Prediction**: Real-time system performance

---

## Sample Output

### Disk Scheduling Comparison

```
FCFS:   109 seeks (total movement)
SSTF:    45 seeks ← Best
SCAN:    95 seeks
C-SCAN:  85 seeks
```

### Search Algorithm Comparison

```
Linear Search:  1000 comparisons
Binary Search: 10 comparisons
Speedup: 100x faster with Binary Search
```

### ML Prediction

```
Prediction: Good
Confidence: 93%
System Status: Performance is optimal
```

---

## Technologies Used

| Technology   | Purpose            |
| ------------ | ------------------ |
| Flask        | Web framework      |
| SQLAlchemy   | Database ORM       |
| SQLite       | Database (default) |
| psutil       | System metrics     |
| scikit-learn | ML classification  |
| Chart.js     | Real-time charts   |
| HTML/CSS/JS  | Frontend UI        |

---

## Troubleshooting

### Port already in use

```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Database issues

```bash
# Delete database to reset
rm disk_io.db
```

### Missing dependencies

```bash
# Reinstall requirements
pip install -r requirements.txt
```

---

## Future Enhancements

1. Add MySQL support for real DBMS testing
2. Implement more ML models (Decision Tree, KNN)
3. Add real-time notifications for poor performance
4. Export metrics to CSV/Excel
5. Add user authentication
6. Implement actual disk I/O benchmarks

---

## License

This project is for educational purposes.

---

## Author

Created as a mini project demonstrating OS, DBMS, DAA, and ML concepts.
