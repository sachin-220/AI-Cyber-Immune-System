import serial
import threading
import json
import csv
from datetime import datetime
from flask import Flask, jsonify, render_template_string

# =============================
# CONFIGURATION
# =============================

# Change this to your COM port
SERIAL_PORT = 'COM6'
BAUD_RATE = 115200
CSV_FILE = 'trust_logs.csv'

# =============================
# SERIAL SETUP
# =============================

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

latest_data = {
    "device_count": 0,
    "risk_weightage": 0,
    "trust_score": 0
}

data_history = []  # store last 50 points for graph

# =============================
# FUNCTION TO READ SERIAL
# =============================

def read_serial():
    global latest_data, data_history
    buffer = ""

    while True:
        line = ser.readline().decode(errors='ignore').strip()

        # Start of JSON
        if line.startswith("{"):
            buffer = line
            continue

        # Append lines until closing brace
        if buffer != "":
            buffer += line
            if line.endswith("}"):
                try:
                    clean_json = buffer.replace("'", "\"")
                    parsed = json.loads(clean_json)
                    latest_data = parsed

                    # Add timestamp
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    entry = {
                        "time": timestamp,
                        "device_count": parsed.get("device_count",0),
                        "risk_weightage": parsed.get("risk_weightage",0),
                        "trust_score": parsed.get("trust_score",0)
                    }

                    data_history.append(entry)
                    if len(data_history) > 50:
                        data_history.pop(0)  # keep last 50 points

                    # Save to CSV
                    with open(CSV_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp,
                                         entry["device_count"],
                                         entry["risk_weightage"],
                                         entry["trust_score"]])

                except:
                    pass
                buffer = ""

# Start serial reading thread
thread = threading.Thread(target=read_serial)
thread.daemon = True
thread.start()

# =============================
# FLASK DASHBOARD
# =============================

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>AUTO SHIELD Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
let chart;
function fetchData(){
    fetch('/data')
    .then(res => res.json())
    .then(data => {
        document.getElementById("devices").innerHTML = data.device_count;
        document.getElementById("risk").innerHTML = data.risk_weightage;
        document.getElementById("trust").innerHTML = data.trust_score;

        // Background color
        if(data.trust_score >= 80)
            document.body.style.backgroundColor = "#0f0";
        else if(data.trust_score >= 50)
            document.body.style.backgroundColor = "#ff0";
        else
            document.body.style.backgroundColor = "#f00";

        // Update chart
        if(chart){
            chart.data.labels = data.history.map(x => x.time);
            chart.data.datasets[0].data = data.history.map(x => x.trust_score);
            chart.update();
        }
    });
}

window.onload = function(){
    fetchData();
    setInterval(fetchData, 2000);

    const ctx = document.getElementById('trustChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Trust Score',
                data: [],
                borderColor: 'blue',
                backgroundColor: 'rgba(0,0,255,0.1)',
                fill: true,
            }]
        },
        options: {
            responsive:true,
            animation:false,
            scales:{
                y: { min:0, max:100 }
            }
        }
    });
}
</script>
</head>
<body style="text-align:center;font-family:Arial">
<h1>🔥 AUTO SHIELD DASHBOARD</h1>
<h2>Devices: <span id="devices">0</span></h2>
<h2>Risk Weightage: <span id="risk">0</span></h2>
<h2>Trust Score: <span id="trust">0</span></h2>
<canvas id="trustChart" width="800" height="400"></canvas>
</body>
</html>
""")

@app.route("/data")
def data():
    # return latest data + history for graph
    return jsonify({
        "device_count": latest_data.get("device_count",0),
        "risk_weightage": latest_data.get("risk_weightage",0),
        "trust_score": latest_data.get("trust_score",0),
        "history": data_history
    })

# =============================
# RUN FLASK
# =============================

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)