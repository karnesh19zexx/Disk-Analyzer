import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

def create_dataset():
    np.random.seed(42)
    samples = []
    
    for _ in range(100):
        cpu = np.random.uniform(0, 40)
        ram = np.random.uniform(0, 50)
        disk = np.random.uniform(0, 60)
        samples.append([cpu, ram, disk, 0])
    
    for _ in range(100):
        cpu = np.random.uniform(40, 75)
        ram = np.random.uniform(50, 80)
        disk = np.random.uniform(60, 85)
        samples.append([cpu, ram, disk, 1])
    
    for _ in range(100):
        cpu = np.random.uniform(75, 100)
        ram = np.random.uniform(80, 100)
        disk = np.random.uniform(85, 100)
        samples.append([cpu, ram, disk, 2])
    
    return np.array(samples)

def train_model():
    data = create_dataset()
    X = data[:, :3]
    y = data[:, 3]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/disk_analyzer.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')
    
    return model, scaler

def load_trained_model():
    model_path = 'model/disk_analyzer.pkl'
    scaler_path = 'model/scaler.pkl'
    
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    else:
        model, scaler = train_model()
    
    return model, scaler

def predict_health(cpu, ram, disk):
    model, scaler = load_trained_model()
    
    features = np.array([[cpu, ram, disk]])
    features_scaled = scaler.transform(features)
    
    prediction = model.predict(features_scaled)[0]
    
    labels = {0: 'Healthy', 1: 'Warning', 2: 'Critical'}
    return labels[int(prediction)]