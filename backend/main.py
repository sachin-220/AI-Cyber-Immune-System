from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import json
from datetime import datetime
import hashlib
import os
import psutil
import threading
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from fastapi import UploadFile, File, Form
import csv
import io

def decrypt_data(encrypted_data, key):
    """Decrypt AES-256-CBC encrypted data"""
    try:
        iv_hex, encrypted_hex = encrypted_data.split(':', 1)
        iv = bytes.fromhex(iv_hex)
        encrypted = bytes.fromhex(encrypted_hex)
        
        # Derive key using scrypt
        kdf = Scrypt(salt=b'salt', length=32, n=2**14, r=8, p=1, backend=default_backend())
        derived_key = kdf.derive(key.encode())
        
        cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_len = decrypted_padded[-1]
        decrypted = decrypted_padded[:-padding_len]
        
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

app = FastAPI(title="AutoShield Backend", description="Adaptive Cyber-Physical Zero Trust Security Architecture")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Company data
companies = {
    "CompanyA": {"rank": 8.5, "alerts": []},
    "CompanyB": {"rank": 7.2, "alerts": []},
    "CompanyC": {"rank": 9.1, "alerts": []}
}

current_company = None

# Models
class TelemetryData(BaseModel):
    device_id: str
    rssi: float
    probe_requests: int
    environmental_data: dict
    trust_score: float
    timestamp: str

class ThreatEvent(BaseModel):
    event_type: str
    severity: str
    description: str
    mitre_technique: str
    stix_category: str

# In-memory storage (in production, use database)
telemetry_store = [
    {"device_id": "esp32_001", "rssi": -45, "probe_requests": 5, "environmental_data": {"temperature": 22.5, "humidity": 55.0}, "trust_score": 0.85, "timestamp": "2026-02-21T10:00:00Z"},
    {"device_id": "esp32_002", "rssi": -60, "probe_requests": 12, "environmental_data": {"temperature": 23.0, "humidity": 60.0}, "trust_score": 0.65, "timestamp": "2026-02-21T10:05:00Z"}
]
threat_store = [
    {"event_type": "anomaly_detected", "severity": "medium", "description": "Unusual probe requests detected", "mitre_technique": "T1071", "stix_category": "network-traffic-analysis"}
]
blockchain_ledger = [
    {"hash": "abc123...", "timestamp": "2026-02-21T10:00:00Z", "metadata": "threat_logged"}
]
endpoint_monitoring = []

@app.post("/telemetry")
async def receive_telemetry(data: dict):
    """Receive encrypted telemetry data from ESP32 rover"""
    print("Received telemetry data:", data)  # Debug log
    encrypted_data = data.get("encrypted_data", "")
    decrypted_info = None
    if encrypted_data:
        # Decrypt AES
        decrypted = decrypt_data(encrypted_data, "AutoShieldKey123")
        if decrypted:
            decrypted_info = json.loads(decrypted)
            print("Decrypted data:", decrypted_info)  # Debug log
    
    # Store full data
    telemetry_store.append(data)
    
    # Use decrypted info for analysis if available
    analysis_data = decrypted_info if decrypted_info else data
    
    # Threat Analysis Engine
    trust_score = analysis_data.get("trust_score", 100)
    device_count = analysis_data.get("device_count", 0)
    risk_weightage = analysis_data.get("risk_weightage", 0)
    temperature = data.get("temperature", 25)  # From full data
    humidity = data.get("humidity", 60)
    posture_issues = data.get("posture_issues", [])
    physical_attacker = data.get("physical_attacker", False)
    
    threat_level = "LOW"
    if trust_score < 50:
        threat_level = "HIGH"
    elif trust_score < 80:
        threat_level = "MEDIUM"
    
    if risk_weightage > 20:  # Threshold
        threat_level = "CRITICAL"
    
    # Map to MITRE and STIX
    mitre_technique = "T1071"  # Default
    stix_category = "network-traffic-analysis"
    
    if threat_level in ["HIGH", "CRITICAL"]:
        mitre_technique = "T1021"  # Remote Services
        stix_category = "lateral-movement"
    
    if trust_score < 0.5:
        threat = {
            "event_type": "anomaly_detected",
            "severity": threat_level,
            "description": f"Low trust score detected for device {data.get('device_id', 'unknown')}",
            "mitre_technique": mitre_technique,
            "stix_category": stix_category
        }
        threat_store.append(threat)
        # Log to blockchain
        log_to_blockchain(json.dumps(threat))
        
        # Auto Response Engine
        if threat["severity"] in ["HIGH", "CRITICAL"]:
            auto_response(threat)
    
    return {"status": "received", "processed": True}

def auto_response(threat):
    """Auto Response Engine"""
    actions = []
    if "anomaly" in threat["event_type"]:
        actions.append("block_ip")
        actions.append("isolate_device")
    if threat["severity"] == "CRITICAL":
        actions.append("micro_segment")
        actions.append("activate_honeypot")
    
    for action in actions:
        # Simulate response
        print(f"Auto Response: {action} triggered for threat {threat['description']}")
    
    return actions

endpoint_monitoring = []

# Endpoint Behavioral Agent
def endpoint_behavioral_monitor():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": cpu,
            "memory_usage": memory,
            "anomaly": (cpu > 85 or memory > 85)
        }
        
        endpoint_monitoring.append(data)
        
        if data["anomaly"]:
            threat = {
                "event_type": "endpoint_anomaly",
                "severity": "high",
                "description": f"High resource usage detected: CPU {cpu}%, Memory {memory}%",
                "mitre_technique": "T1490",  # Inhibit System Recovery
                "stix_category": "impact"
            }
            threat_store.append(threat)
            log_to_blockchain(json.dumps(threat))
        
        time.sleep(30)  # Check every 30 seconds

@app.get("/threats")
async def get_threats():
    """Get recent threat events"""
    return {"threats": threat_store[-10:]}  # Last 10 threats

@app.get("/telemetry")
async def get_telemetry():
    """Get recent telemetry data"""
    return {"telemetry": telemetry_store[-50:]}  # Last 50 entries

@app.get("/endpoint")
async def get_endpoint_monitoring():
    """Get endpoint behavioral monitoring data"""
    return {"endpoint_data": endpoint_monitoring[-20:]}  # Last 20 entries

@app.get("/zkp")
async def get_zero_knowledge_proof():
    """Simulate Zero Knowledge Proof - share hash without raw data"""
    if telemetry_store:
        latest = telemetry_store[-1]
        data_hash = hashlib.sha256(json.dumps(latest, sort_keys=True).encode()).hexdigest()
        return {
            "proof": {
                "data_hash": data_hash,
                "threat_indicator": "anomaly" if latest.get("trust_score", 100) < 80 else "normal",
                "risk_score": latest.get("risk_score", 0),
                "verification": "Hash matches internal data without revealing content"
            }
        }
    return {"proof": "No data available"}

federated_models = []  # Store received model weights

@app.post("/federated")
async def receive_federated_weights(data: dict):
    """Receive federated learning weights from organizations"""
    weights = data.get("weights", [])
    federated_models.append(weights)
    
    # Simple aggregation: average weights
    if len(federated_models) > 1:
        global_weights = []
        for i in range(len(weights)):
            avg = sum(model[i] for model in federated_models) / len(federated_models)
            global_weights.append(avg)
        # Update global model (simulation)
        print("Global model updated with federated weights")
    
    return {"status": "weights_received", "global_updated": True}

def log_to_blockchain(threat_data):
    """Simulate blockchain logging with hash"""
    threat_json = json.dumps(threat_data, sort_keys=True)
    threat_hash = hashlib.sha256(threat_json.encode()).hexdigest()
    entry = {
        "hash": threat_hash,
        "timestamp": datetime.now().isoformat(),
        "metadata": "threat_logged"
    }
    blockchain_ledger.append(entry)

@app.get("/blockchain")
async def get_blockchain():
    """Get blockchain ledger"""
    return {"ledger": blockchain_ledger}

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    global current_company
    if not current_company:
        return {"error": "Please login first"}
    
    try:
        content = await file.read()
        data_type = "unknown"
        analysis = {}
        
        # Detect file type
        if file.filename.endswith('.csv'):
            data_type = "CSV Security Logs"
            # Parse CSV
            csv_reader = csv.DictReader(io.StringIO(content.decode('utf-8')))
            rows = list(csv_reader)
            analysis = analyze_security_data(rows)
        elif file.filename.endswith('.json'):
            data_type = "JSON Threat Intelligence"
            json_data = json.loads(content)
            analysis = analyze_security_data(json_data if isinstance(json_data, list) else [json_data])
        else:
            data_type = "Unknown Format"
            analysis = {"error": "Unsupported file format"}
        
        # Update company rank
        if "score" in analysis:
            companies[current_company]["rank"] = analysis["score"]
        
        # Send alerts to other companies
        alert_message = f"Security update from {current_company}: {analysis.get('summary', 'Data analyzed')}"
        for comp in companies:
            if comp != current_company:
                companies[comp]["alerts"].append({
                    "from": current_company,
                    "message": alert_message,
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "company": current_company,
            "data_type": data_type,
            "analysis": analysis,
            "rank": companies[current_company]["rank"]
        }
    except Exception as e:
        return {"error": str(e)}

def analyze_security_data(data):
    """Analyze security data and compute metrics"""
    if not data:
        return {"error": "No data to analyze"}
    
    # Basic analysis
    total_records = len(data)
    threat_count = 0
    anomaly_count = 0
    risk_score = 0
    
    for record in data:
        if isinstance(record, dict):
            # Check for threat indicators
            if any(key.lower() in ['threat', 'attack', 'malware', 'anomaly'] for key in record.keys()):
                threat_count += 1
            if 'risk' in record and isinstance(record['risk'], (int, float)):
                risk_score += record['risk']
            if 'anomaly' in record and record['anomaly']:
                anomaly_count += 1
    
    # Compute security score (0-10)
    base_score = 10
    if threat_count > 0:
        base_score -= min(threat_count * 0.5, 3)
    if anomaly_count > 0:
        base_score -= min(anomaly_count * 0.3, 2)
    if risk_score > 0:
        avg_risk = risk_score / total_records
        base_score -= min(avg_risk / 10, 2)
    
    security_score = max(0, min(10, base_score))
    
    return {
        "total_records": total_records,
        "threats_detected": threat_count,
        "anomalies_detected": anomaly_count,
        "average_risk": risk_score / total_records if total_records > 0 else 0,
        "score": round(security_score, 1),
        "summary": f"Analyzed {total_records} records. Security Score: {security_score:.1f}/10"
    }

@app.get("/companies")
async def get_companies():
    return {"companies": companies, "current": current_company}

@app.get("/alerts")
async def get_alerts():
    if not current_company:
        return {"error": "Please login first"}
    return {"alerts": companies[current_company]["alerts"]}

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoShield Login</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); width: 400px; }
        h1 { text-align: center; color: #333; margin-bottom: 30px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #5a6fd8; }
        .security-note { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🔒 AutoShield Login</h1>
        <form action="/login" method="post">
            <input type="text" name="company" placeholder="Enter Company Name" required>
            <button type="submit">Access Security Dashboard</button>
        </form>
        <div class="security-note">
            <p>🛡️ Advanced Zero-Trust Security Immune System</p>
            <p>Multi-Organization Threat Intelligence & Ranking</p>
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=login_html)

@app.post("/login")
async def login(company: str = Form(...)):
    global current_company
    current_company = company
    if company not in companies:
        companies[company] = {"rank": 5.0, "alerts": []}
    return {"redirect": "/"}

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoShield Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { display: flex; flex-wrap: wrap; }
        .panel { width: 45%; margin: 10px; padding: 20px; border: 1px solid #ccc; border-radius: 5px; }
        canvas { max-width: 100%; }
    </style>
</head>
<body>
    <h1>AutoShield SOC Dashboard</h1>
    <div id="company-info" style="background: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 5px;">
        <h3>Company: <span id="company-name">Loading...</span></h3>
        <p>Security Rank: <span id="company-rank">Loading...</span>/10</p>
        <button onclick="showAlerts()">View Alerts</button>
    </div>
    <div class="panel" style="width: 100%;">
        <h2>Data Analysis & Ranking</h2>
        <input type="file" id="fileInput" accept=".csv,.json">
        <button onclick="analyzeFile()">Analyze Security Data</button>
        <div id="analysis-result" style="margin-top: 10px;"></div>
    </div>
    <div class="container">
        <div class="panel">
            <h2>Trust Score Trends</h2>
            <canvas id="trustChart"></canvas>
        </div>
        <div class="panel">
            <h2>Recent Threats</h2>
            <ul id="threatsList"></ul>
        </div>
        <div class="panel">
            <h2>Telemetry Data</h2>
            <canvas id="telemetryChart"></canvas>
        </div>
        <div class="panel">
            <h2>Rover Analysis</h2>
            <div id="roverAnalysis">
                <p>Loading rover data...</p>
            </div>
        </div>
        <div class="panel">
            <h2>Endpoint Monitoring</h2>
            <canvas id="endpointChart"></canvas>
        </div>
        <div class="panel">
            <h2>Threat Timeline</h2>
            <ul id="threatTimeline"></ul>
        </div>

    <script>
        const backendURL = '';

        async function fetchData(endpoint) {
            const response = await fetch(`${backendURL}${endpoint}`);
            return await response.json();
        }

        async function loadCompanyInfo() {
            try {
                const data = await fetchData('/companies');
                document.getElementById('company-name').textContent = data.current || 'Unknown';
                document.getElementById('company-rank').textContent = data.companies[data.current]?.rank || 'N/A';
            } catch (e) {
                console.error('Failed to load company info:', e);
            }
        }

        async function analyzeFile() {
            const fileInput = document.getElementById('fileInput');
            const resultDiv = document.getElementById('analysis-result');
            
            if (!fileInput.files[0]) {
                resultDiv.innerHTML = '<p style="color: red;">Please select a file first.</p>';
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (result.error) {
                    resultDiv.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <h3>Analysis Complete</h3>
                        <p><strong>Data Type:</strong> ${result.data_type}</p>
                        <p><strong>Records Analyzed:</strong> ${result.analysis.total_records}</p>
                        <p><strong>Threats Detected:</strong> ${result.analysis.threats_detected}</p>
                        <p><strong>Security Score:</strong> ${result.analysis.score}/10</p>
                        <p><strong>Updated Rank:</strong> ${result.rank}/10</p>
                        <p style="color: green;">✅ Alerts sent to other organizations</p>
                    `;
                    loadCompanyInfo(); // Refresh rank
                }
            } catch (e) {
                resultDiv.innerHTML = `<p style="color: red;">Analysis failed: ${e.message}</p>`;
            }
        }

        async function showAlerts() {
            try {
                const data = await fetchData('/alerts');
                const alerts = data.alerts || [];
                alert('Recent Alerts:\\n' + alerts.slice(-3).map(a => `${a.timestamp}: ${a.message}`).join('\\n'));
            } catch (e) {
                alert('Failed to load alerts');
            }
        }

        async function updateDashboard() {
            loadCompanyInfo();
            // Fetch telemetry
            const telemetryData = await fetchData('/telemetry');
            const threatsData = await fetchData('/threats');
            const ledgerData = await fetchData('/blockchain');
            const endpointData = await fetchData('/endpoint');

            // Update trust score chart
            const trustCtx = document.getElementById('trustChart').getContext('2d');
            const trustScores = telemetryData.telemetry.map(t => t.trust_score);
            const timestamps = telemetryData.telemetry.map(t => new Date(t.timestamp).toLocaleTimeString());
            
            new Chart(trustCtx, {
                type: 'line',
                data: {
                    labels: timestamps,
                    datasets: [{
                        label: 'Trust Score',
                        data: trustScores,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                }
            });

            // Update threats list
            const threatsList = document.getElementById('threatsList');
            threatsList.innerHTML = '';
            threatsData.threats.slice(-5).forEach(threat => {
                const li = document.createElement('li');
                li.textContent = `${threat.event_type}: ${threat.description} (${threat.severity})`;
                threatsList.appendChild(li);
            });

            // Update threat timeline
            const threatTimeline = document.getElementById('threatTimeline');
            threatTimeline.innerHTML = '';
            threatsData.threats.forEach(threat => {
                const li = document.createElement('li');
                li.textContent = `${threat.timestamp || 'N/A'}: ${threat.description}`;
                threatTimeline.appendChild(li);
            });

            // Update telemetry chart
            const telCtx = document.getElementById('telemetryChart').getContext('2d');
            const deviceCounts = telemetryData.telemetry.map(t => t.device_count || 0);
            const temperatures = telemetryData.telemetry.map(t => t.temperature || 25);
            
            new Chart(telCtx, {
                type: 'line',
                data: {
                    labels: timestamps,
                    datasets: [{
                        label: 'Device Count',
                        data: deviceCounts,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }, {
                        label: 'Temperature (°C)',
                        data: temperatures,
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.1
                    }]
                }
            });

            // Update rover analysis
            const roverDiv = document.getElementById('roverAnalysis');
            const latestTelemetry = telemetryData.telemetry[telemetryData.telemetry.length - 1];
            if (latestTelemetry) {
                roverDiv.innerHTML = `
                    <h3>Latest Rover Output</h3>
                    <p><strong>Device Count:</strong> ${latestTelemetry.device_count || 'N/A'}</p>
                    <p><strong>Risk Weightage:</strong> ${latestTelemetry.risk_weightage || 'N/A'}</p>
                    <p><strong>Trust Score:</strong> ${latestTelemetry.trust_score || 'N/A'}</p>
                    <p><strong>Temperature:</strong> ${latestTelemetry.temperature ? latestTelemetry.temperature.toFixed(1) + '°C' : 'N/A'}</p>
                    <p><strong>Humidity:</strong> ${latestTelemetry.humidity ? latestTelemetry.humidity.toFixed(1) + '%' : 'N/A'}</p>
                    <p><strong>Posture Issues:</strong> ${latestTelemetry.posture_issues && latestTelemetry.posture_issues.length > 0 ? latestTelemetry.posture_issues.join(', ') : 'None'}</p>
                    <p><strong>Physical Attacker Detected:</strong> ${latestTelemetry.physical_attacker ? 'YES' : 'NO'}</p>
                    <p><strong>Timestamp:</strong> ${latestTelemetry.timestamp ? new Date(latestTelemetry.timestamp).toLocaleString() : 'N/A'}</p>
                `;
            } else {
                roverDiv.innerHTML = '<p>No rover data available</p>';
            }

            // Update endpoint chart
            const endpointCtx = document.getElementById('endpointChart').getContext('2d');
            const cpuValues = endpointData.endpoint_data.map(d => d.cpu_usage);
            const memoryValues = endpointData.endpoint_data.map(d => d.memory_usage);
            const endpointTimestamps = endpointData.endpoint_data.map(d => new Date(d.timestamp).toLocaleTimeString());
            
            new Chart(endpointCtx, {
                type: 'line',
                data: {
                    labels: endpointTimestamps,
                    datasets: [{
                        label: 'CPU Usage (%)',
                        data: cpuValues,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }, {
                        label: 'Memory Usage (%)',
                        data: memoryValues,
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.1
                    }]
                }
            });

            // Update ledger
            const ledgerList = document.getElementById('ledgerList');
            ledgerList.innerHTML = '';
            ledgerData.ledger.forEach(entry => {
                const li = document.createElement('li');
                li.textContent = `Hash: ${entry.hash.substring(0, 16)}...`;
                ledgerList.appendChild(li);
            });
        }

        // Update every 10 seconds
        setInterval(updateDashboard, 10000);
        updateDashboard();
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content, status_code=200)

# Start monitoring thread
threading.Thread(target=endpoint_behavioral_monitor, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)