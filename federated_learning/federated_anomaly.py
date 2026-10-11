import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import joblib

# Simulated federated learning for anomaly detection
class FederatedAnomalyDetector:
    def __init__(self):
        self.models = []
        self.global_model = None

    def train_local_model(self, data):
        """Train a local anomaly detection model"""
        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(data)
        return model

    def aggregate_models(self, local_models):
        """Simple model aggregation (in real FL, this would be more sophisticated)"""
        # For simplicity, use the first model as global
        self.global_model = local_models[0]
        return self.global_model

    def predict(self, data):
        """Predict anomalies using global model"""
        if self.global_model is None:
            raise ValueError("No global model available")
        return self.global_model.predict(data)

# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    normal_data = np.random.normal(0, 1, (1000, 2))
    anomaly_data = np.random.normal(5, 1, (100, 2))
    data = np.vstack([normal_data, anomaly_data])
    
    # Simulate multiple organizations
    org1_data, org2_data = train_test_split(data, test_size=0.5, random_state=42)
    
    fl_detector = FederatedAnomalyDetector()
    
    # Train local models
    model1 = fl_detector.train_local_model(org1_data)
    model2 = fl_detector.train_local_model(org2_data)
    
    # Aggregate to global model
    global_model = fl_detector.aggregate_models([model1, model2])
    
    # Save model
    joblib.dump(global_model, 'global_anomaly_model.pkl')
    
    # Test prediction
    test_data = np.random.normal(0, 1, (10, 2))
    predictions = fl_detector.predict(test_data)
    print("Predictions:", predictions)