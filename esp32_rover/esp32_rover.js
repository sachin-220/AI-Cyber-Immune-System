/*
=========================================================
AUTO SHIELD – NODE.JS VERSION
Self Learning Cyber Physical Rover with Zero Trust
Micro-segmentation, Blockchain Encryption, Cloud Integration
=========================================================
*/

const axios = require('axios');
const crypto = require('crypto');

// =============================
// CONFIGURATION
// =============================

const serverURL = "http://10.248.194.21:8000/telemetry";

// =============================
// SIMULATED LED PINS (Console output)
// =============================

const leds = {
    SAFE_LED: false,
    SUSPICIOUS_LED: false,
    CRITICAL_LED: false,
    PHYSICAL_LED: false
};

// =============================
// SIMULATED DHT CONFIG
// =============================

let temperature = 25.0;
let humidity = 60.0;

// =============================
// TRUST VARIABLES
// =============================

const whitelist = [
    "96:AE:43:36:68:4E"
];

let blacklist = [];
const maxBlacklist = 10;

let trustScore = 100;
let riskWeightage = 0;
let deviceCount = 0;

// Learning system
const learningCycles = 5;
let cycleCounter = 0;

// Risk history
let riskHistory = new Array(15).fill(0);
let historyIndex = 0;

let lastScan = 0;
const scanInterval = 8000;

// Allowed IPs for authentication (simulate)
const allowedIPs = ["192.168.1.100", "192.168.1.101"];

// Encryption key for blockchain
const encryptionKey = "AutoShieldKey123";

// =============================
// UTILITY FUNCTIONS
// =============================

function generateMAC() {
    return Array.from({length: 6}, () => Math.floor(Math.random() * 256).toString(16).padStart(2, '0')).join(':').toUpperCase();
}

function simulateWiFiScan() {
    // Simulate finding random devices
    const devices = [];
    const numDevices = Math.floor(Math.random() * 5) + 1;

    for (let i = 0; i < numDevices; i++) {
        devices.push({
            mac: generateMAC(),
            rssi: -Math.floor(Math.random() * 80) - 20,
            ssid: `Device_${i + 1}`
        });
    }

    return devices;
}

function calculateTrustScore(devices) {
    deviceCount = devices.length;
    let suspiciousCount = 0;
    let criticalCount = 0;

    devices.forEach(device => {
        // Check whitelist
        if (whitelist.includes(device.mac)) {
            return; // Trusted device
        }

        // Check blacklist
        if (blacklist.includes(device.mac)) {
            criticalCount++;
            return;
        }

        // Check signal strength (weak signals might be suspicious)
        if (device.rssi > -50) {
            suspiciousCount++;
        }

        // Simulate behavioral analysis
        if (Math.random() < 0.1) { // 10% chance of anomaly
            suspiciousCount++;
        }
    });

    // Calculate risk weightage
    riskWeightage = (suspiciousCount * 20) + (criticalCount * 50);

    // Update trust score
    trustScore = Math.max(0, 100 - riskWeightage);

    // Learning: adjust based on history
    if (cycleCounter >= learningCycles) {
        const avgRisk = riskHistory.reduce((a, b) => a + b, 0) / riskHistory.length;
        if (avgRisk > 30) {
            trustScore *= 0.95; // Reduce trust if consistently high risk
        }
    }

    // Store in history
    riskHistory[historyIndex] = riskWeightage;
    historyIndex = (historyIndex + 1) % 15;

    cycleCounter++;
}

function updateLEDs() {
    // Reset all LEDs
    Object.keys(leds).forEach(key => leds[key] = false);

    if (trustScore >= 80) {
        leds.SAFE_LED = true;
    } else if (trustScore >= 50) {
        leds.SUSPICIOUS_LED = true;
    } else {
        leds.CRITICAL_LED = true;
    }

    // Simulate physical attacker detection
    if (Math.random() < 0.05) { // 5% chance
        leds.PHYSICAL_LED = true;
    }

    console.log('LED Status:', leds);
}

function readDHT() {
    // Simulate DHT sensor readings
    temperature += (Math.random() - 0.5) * 2; // Small variations
    humidity += (Math.random() - 0.5) * 5;

    // Keep in reasonable ranges
    temperature = Math.max(15, Math.min(35, temperature));
    humidity = Math.max(30, Math.min(90, humidity));

    return { temperature, humidity };
}

function encryptData(data) {
    const algorithm = 'aes-256-cbc';
    const key = crypto.scryptSync(encryptionKey, 'salt', 32);
    const iv = crypto.randomBytes(16);

    const cipher = crypto.createCipheriv(algorithm, key, iv);
    let encrypted = cipher.update(JSON.stringify(data), 'utf8', 'hex');
    encrypted += cipher.final('hex');

    // Return encrypted data with IV for decryption
    return iv.toString('hex') + ':' + encrypted;
}

function dynamicBlacklisting(devices) {
    devices.forEach(device => {
        if (!whitelist.includes(device.mac) && !blacklist.includes(device.mac)) {
            if (Math.random() < 0.1) { // 10% chance to blacklist suspicious device
                if (blacklist.length < maxBlacklist) {
                    blacklist.push(device.mac);
                    console.log(`🚫 Blacklisted suspicious device: ${device.mac}`);
                }
            }
        }
    });
}

function postureCheck() {
    // Simulate posture checks
    const postureIssues = [];

    if (temperature > 30) {
        postureIssues.push("High temperature detected");
    }

    if (humidity > 80) {
        postureIssues.push("High humidity detected");
    }

    if (trustScore < 50) {
        postureIssues.push("Low trust score");
    }

    return postureIssues;
}

function detectPhysicalAttacker() {
    // Simulate PIR sensor
    return Math.random() < 0.05; // 5% chance of detection
}

async function sendToBackend(data) {
    try {
        const response = await axios.post(serverURL, data);
        console.log('✅ Data sent to backend:', response.status);
    } catch (error) {
        console.error('❌ Failed to send data:', error.message);
    }
}

// =============================
// MAIN LOOP
// =============================

async function main() {
    console.log('\n🔥 AUTO SHIELD STARTING - Zero Trust Mode (Node.js)');

    // Simulate WiFi connection
    console.log('📡 Connecting to WiFi...');
    console.log('✅ Connected to Sanjuu');

    // Simulate honeypot
    console.log('🔥 Honeypot Active - Trapping Unauthorized Connections');

    while (true) {
        const now = Date.now();

        if (now - lastScan >= scanInterval) {
            console.log('\n🔍 Scanning for devices...');

            // Simulate WiFi scan
            const devices = simulateWiFiScan();
            console.log(`📱 Found ${devices.length} devices:`, devices.map(d => d.mac));

            // Calculate trust
            calculateTrustScore(devices);

            // Dynamic blacklisting
            dynamicBlacklisting(devices);

            // Update LEDs
            updateLEDs();

            // Read sensors
            const dhtData = readDHT();
            console.log(`🌡️ Temperature: ${dhtData.temperature.toFixed(1)}°C, Humidity: ${dhtData.humidity.toFixed(1)}%`);

            // Posture check
            const postureIssues = postureCheck();
            if (postureIssues.length > 0) {
                console.log('⚠️ Posture Issues:', postureIssues);
            }

            // Physical attacker detection
            const physicalAttacker = detectPhysicalAttacker();
            if (physicalAttacker) {
                console.log('🚨 Physical attacker detected!');
            }

            // Prepare data for backend
            const telemetryData = {
                device_count: deviceCount,
                risk_weightage: riskWeightage,
                trust_score: trustScore,
                temperature: dhtData.temperature,
                humidity: dhtData.humidity,
                posture_issues: postureIssues,
                physical_attacker: physicalAttacker,
                timestamp: new Date().toISOString(),
                encrypted_data: encryptData({
                    devices: devices.map(d => ({ mac: d.mac, rssi: d.rssi })),
                    trust_score: trustScore
                })
            };

            // Send to backend
            await sendToBackend(telemetryData);

            lastScan = now;
        }

        // Small delay
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

// =============================
// START
// =============================

main().catch(console.error);