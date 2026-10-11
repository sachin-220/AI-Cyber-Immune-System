# AutoShield: Adaptive Cyber-Physical Zero Trust Security Architecture

## Overview

AutoShield is a comprehensive cybersecurity framework that combines edge intelligence, behavioral anomaly detection, federated learning, blockchain-based threat logging, and automated response mechanisms into a unified security ecosystem. Now enhanced with Zero Trust continuous verification, micro-segmentation simulation, cloud-optimized processing via Nvidia GPU Cloud, and physical attacker monitoring.

## Architecture

### Layer 1: ESP32 Rover (Edge Intelligence)
- **Zero Trust Continuous Verification**: MAC/RSSI fingerprinting with persistent trust scoring
- **Micro-segmentation**: ESP32 VLAN simulation via multiple SSID segregation
- **Cyber-physical Sensors**: DHT11 temp/humidity fusion into risk model with multi-sensor anomaly weighting
- **Persistent Trust Engine**: Memory buffer with learning cycles for stability
- **Behavioral Analysis + Honeypot**: SoftAP mode for trapping unauthorized connections
- **Automated Reset Cycles**: Self-healing on critical states
- **LED Status Indicators**: Rapid response visualization
- **Physical Attacker Monitoring**: Environmental anomaly detection for intrusion alerts
- **Dynamic Device Blacklisting**: Based on RSSI/anomaly scores
- **NAC with Posture Checks**: Device compliance verification
- **IP Address Authentication**: Without accessing company data
- **Simulated Abnormal Traffic Detection**: Packet anomaly monitoring
- **JSON Exports**: Device count, risk score for cloud/SIEM integration
- **Blockchain Encryption**: Data encrypted before transmission

### Layer 2: Cloud Backend (Intelligence Engine)
- **Cloud-Optimized Processing**: Nvidia GPU Cloud for advanced ML/AI analysis
- Threat classification and analysis
- Tamper-resistant blockchain ledger
- Automated response mechanisms (isolate, block, micro-segment)
- Federated learning for collaborative model improvement
- Zero Knowledge verification (no company data access)
- SOC-style dashboard with live visualization

## Components

- `esp32_rover/`: Enhanced ESP32 firmware with all security features
- `backend/`: FastAPI-based cloud intelligence engine
- `frontend/`: SOC-style dashboard (served from backend)
- `blockchain/`: Threat ledger implementation
- `federated_learning/`: Collaborative anomaly detection models

## Setup

### ESP32 Setup
1. Install Arduino IDE with ESP32 board support
2. Install libraries: WiFi, HTTPClient, ArduinoJson, DHT
3. Update WiFi credentials and server URL in code
4. Upload to ESP32 board
5. Connect DHT11 to pin 23, LEDs to pins 18,19,21,22

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Cloud Deployment
- Deploy backend to Nvidia GPU Cloud for optimized processing
- Use federated learning for model updates without data sharing

## Features

- Real-time telemetry collection with encryption
- Behavioral anomaly detection with multi-sensor fusion
- Automated threat response and self-healing
- Decentralized threat logging with blockchain
- Federated model training across organizations
- SOC dashboard with live attack telemetry
- Physical and cyber threat monitoring
- Zero Trust architecture with continuous verification
- Cloud-optimized AI/ML processing

## Security Features

- Zero Trust continuous verification
- Micro-segmentation simulation
- Device isolation and blacklisting
- Honeypot activation
- MITRE ATT&CK mapping
- STIX-compatible categorization
- Encrypted data transmission
- No company data access for privacy