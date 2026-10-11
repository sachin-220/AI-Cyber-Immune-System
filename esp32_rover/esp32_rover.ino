/*
=========================================================
AUTO SHIELD – ENHANCED VERSION
Self Learning Cyber Physical Rover with Zero Trust
Micro-segmentation, Blockchain Encryption, Cloud Integration
=========================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// =============================
// WIFI CONFIG
// =============================

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverURL = "http://10.248.194.21:8000/telemetry";  // Updated with local IP

// =============================
// LED PINS
// =============================

#define SAFE_LED 18
#define SUSPICIOUS_LED 19
#define CRITICAL_LED 21
#define PHYSICAL_LED 22

// =============================
// DHT CONFIG
// =============================

#define DHTPIN 23
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// =============================
// TRUST VARIABLES
// =============================

String whitelist[] = {
  "96:AE:43:36:68:4E"
};

String blacklist[10];  // Dynamic blacklist
int blacklistCount = 0;

float trustScore = 100;
float riskWeightage = 0;
int deviceCount = 0;

// Learning system
int learningCycles = 5;
int cycleCounter = 0;

// Risk history
float riskHistory[15];
int historyIndex = 0;

unsigned long lastScan = 0;
const int scanInterval = 8000;

// Allowed IPs for authentication (simulate)
String allowedIPs[] = {"192.168.1.100", "192.168.1.101"};

// Encryption key for blockchain
const char* encryptionKey = "AutoShieldKey123";

// =====================================================
// SETUP
// =====================================================

void setup() {

  Serial.begin(115200);

  pinMode(SAFE_LED, OUTPUT);
  pinMode(SUSPICIOUS_LED, OUTPUT);
  pinMode(CRITICAL_LED, OUTPUT);
  pinMode(PHYSICAL_LED, OUTPUT);

  dht.begin();

  Serial.println("\n🔥 AUTO SHIELD STARTING - Zero Trust Mode");

  connectWiFi();

  WiFi.softAP("Company_Security_Honeypot", "honeypot123");  // Honeypot with password

  Serial.println("🔥 Honeypot Active - Trapping Unauthorized Connections");

  // Initialize risk history
  for (int i = 0; i < 15; i++) {
    riskHistory[i] = 0;
  }
}

// =====================================================
// LOOP
// =====================================================

void loop() {

  if (millis() - lastScan > scanInterval) {

    Serial.println("\n==============================");
    Serial.println(" SECURITY ANALYSIS CYCLE ");
    Serial.println("==============================");

    riskWeightage = 0;

    deviceCount = scanDevices();
    behavioralAnalysis();
    environmentalAnalysis();
    physicalAttackerDetection();  // New: Detect physical attackers

    applyLearningMemory();
    calculateTrust();

    cycleCounter++;

    if (cycleCounter <= learningCycles) {

      Serial.println("🔵 LEARNING MODE (Calibration Phase)");
      printStructuredOutput();
      lastScan = millis();
      return;
    }

    decisionEngine();
    dynamicBlacklisting();  // New: Blacklist based on scores
    printStructuredOutput();
    sendToCloud();  // New: Send encrypted data to cloud

    lastScan = millis();
  }
}

// =====================================================
// WIFI CONNECTION
// =====================================================

void connectWiFi() {

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  int timeout = 20;

  while (WiFi.status() != WL_CONNECTED && timeout > 0) {

    delay(500);
    Serial.print(".");
    timeout--;
  }

  if (WiFi.status() == WL_CONNECTED) {

    Serial.println("\n✅ WiFi Connected");
    Serial.println(WiFi.localIP());

  } else {

    Serial.println("\n❌ WiFi Failed");
  }
}

// =====================================================
// DEVICE SCANNING
// =====================================================

int scanDevices() {

  Serial.println("\n[Device Fingerprinting - Zero Trust]");

  int networks = WiFi.scanNetworks();

  Serial.print("Devices Found: ");
  Serial.println(networks);

  for (int i = 0; i < networks; i++) {

    String mac = WiFi.BSSIDstr(i);
    int rssi = WiFi.RSSI(i);
    String ssid = WiFi.SSID(i);

    Serial.print("MAC: ");
    Serial.print(mac);
    Serial.print(" | RSSI: ");
    Serial.print(rssi);
    Serial.print(" | SSID: ");
    Serial.println(ssid);

    // Zero Trust: Continuous verification
    if (isBlacklisted(mac)) {
      riskWeightage += 10;  // High penalty for blacklisted
      Serial.println("🚨 Blacklisted Device Detected");
    } else if (!isWhitelisted(mac)) {
      riskWeightage += 2;  // Reduced penalty
    }

    // IP Authentication (simulate based on MAC)
    if (!authenticateIP(mac)) {
      riskWeightage += 3;
      Serial.println("🚨 IP Authentication Failed");
    }

    // Anomaly detection
    if (rssi > -35) {
      riskWeightage += 3;  // Possible rogue device
    } else if (rssi < -80) {
      riskWeightage += 1;  // Weak signal, possible interference
    }

    // Posture check (simulate)
    if (!checkPosture(ssid)) {
      riskWeightage += 2;
      Serial.println("🚨 Posture Check Failed");
    }
  }

  WiFi.scanDelete();
  return networks;
}

// =====================================================
// WHITELIST
// =====================================================

bool isWhitelisted(String mac) {

  for (String allowed : whitelist) {

    if (mac == allowed)
      return true;
  }

  return false;
}

// =====================================================
// BLACKLIST
// =====================================================

bool isBlacklisted(String mac) {

  for (int i = 0; i < blacklistCount; i++) {

    if (blacklist[i] == mac)
      return true;
  }

  return false;
}

void addToBlacklist(String mac) {

  if (blacklistCount < 10 && !isBlacklisted(mac)) {
    blacklist[blacklistCount] = mac;
    blacklistCount++;
    Serial.print("🚨 Added to Blacklist: ");
    Serial.println(mac);
  }
}

// =====================================================
// IP AUTHENTICATION
// =====================================================

bool authenticateIP(String mac) {

  // Simulate IP check based on MAC (in real, query DHCP or something)
  // For demo, assume certain MACs have allowed IPs
  if (mac == "96:AE:43:36:68:4E") return true;  // Example
  return false;  // Others fail
}

// =====================================================
// POSTURE CHECK
// =====================================================

bool checkPosture(String ssid) {

  // Simulate posture check: only allow company SSID
  if (ssid == "CompanyWiFi") return true;
  return false;
}

// =====================================================
// BEHAVIOR ANALYSIS
// =====================================================

void behavioralAnalysis() {

  Serial.println("\n[Behavioral Monitoring - Anomaly Detection]");

  int traffic = random(1, 30);
  int abnormalPackets = random(0, 10);

  Serial.print("Traffic Level: ");
  Serial.println(traffic);
  Serial.print("Abnormal Packets: ");
  Serial.println(abnormalPackets);

  if (traffic > 25) {
    riskWeightage += 5;
    Serial.println("🚨 High Traffic Spike");
  }

  if (abnormalPackets > 5) {
    riskWeightage += 4;
    Serial.println("🚨 Abnormal Traffic Detected");
  }

  // Honeypot monitoring
  int honeypotConnections = WiFi.softAPgetStationNum();
  Serial.print("Honeypot Connections: ");
  Serial.println(honeypotConnections);

  if (honeypotConnections > 0) {
    riskWeightage += honeypotConnections * 3;
    Serial.println("🚨 Unauthorized Connections Trapped");
  }
}

// =====================================================
// PHYSICAL ATTACKER DETECTION
// =====================================================

void physicalAttackerDetection() {

  Serial.println("\n[Physical Layer Monitoring]");

  // Simulate physical attacker detection (e.g., via PIR sensor or unusual temp/hum)
  // For demo, use temp/hum anomalies as proxy for physical intrusion

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (!isnan(temp) && !isnan(hum)) {
    if (temp > 45 || hum > 90) {  // Extreme conditions indicate possible physical breach
      riskWeightage += 8;
      Serial.println("🚨 Physical Attacker Suspected - Extreme Environmental Change");
      digitalWrite(PHYSICAL_LED, HIGH);
    }
  }

  // In real, add PIR sensor: if (digitalRead(PIR_PIN) == HIGH) { riskWeightage += 10; }
}

// =====================================================
// LEARNING MEMORY (STABILITY BASELINE)
// =====================================================

void applyLearningMemory() {

  riskHistory[historyIndex] = riskWeightage;
  historyIndex = (historyIndex + 1) % 15;

  float sum = 0;

  for (int i = 0; i < 15; i++) {
    sum += riskHistory[i];
  }

  float mean = sum / 15.0;

  riskWeightage = (riskWeightage + mean) / 2; // Smooth stabilization
}

// =====================================================
// TRUST CALCULATION (FIXED FORMULA)
// =====================================================

void calculateTrust() {

  float normalizedRisk = riskWeightage / (deviceCount + 1);

  trustScore = 100 - (normalizedRisk * 5);

  if (trustScore < 0)
    trustScore = 0;

  Serial.println("\n[Trust Engine]");
  Serial.print("Risk Weightage: ");
  Serial.println(riskWeightage);

  Serial.print("🔥 Trust Score: ");
  Serial.println(trustScore);
}

// =====================================================
// DYNAMIC BLACKLISTING
// =====================================================

void dynamicBlacklisting() {

  // Blacklist devices with low trust or high anomalies
  if (trustScore < 50) {
    // In real, blacklist specific MACs based on analysis
    // For demo, simulate
    Serial.println("🚨 Dynamic Blacklisting Activated");
  }
}

// =====================================================
// SEND TO CLOUD (BLOCKCHAIN ENCRYPTED)
// =====================================================

void sendToCloud() {

  if (WiFi.status() != WL_CONNECTED) return;

  Serial.println("\n[Cloud Integration - Encrypted Transmission]");

  // Create JSON
  StaticJsonDocument<512> doc;
  doc["device_id"] = WiFi.macAddress();
  doc["device_count"] = deviceCount;
  doc["risk_score"] = riskWeightage;
  doc["trust_score"] = trustScore;
  doc["environmental_data"]["temperature"] = dht.readTemperature();
  doc["environmental_data"]["humidity"] = dht.readHumidity();
  doc["timestamp"] = String(millis());
  doc["honeypot_connections"] = WiFi.softAPgetStationNum();

  // Encrypt (simple XOR for demo)
  String jsonString;
  serializeJson(doc, jsonString);
  String encrypted = simpleEncrypt(jsonString, encryptionKey);

  // Send to backend
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST("{\"encrypted_data\":\"" + encrypted + "\"}");

  if (httpResponseCode > 0) {
    Serial.println("✅ Data Sent to Cloud Successfully");
  } else {
    Serial.println("❌ Failed to Send Data");
  }

  http.end();
}

// =====================================================
// SIMPLE ENCRYPTION (FOR BLOCKCHAIN)
// =====================================================

String simpleEncrypt(String data, String key) {

  String encrypted = "";
  for (size_t i = 0; i < data.length(); i++) {
    encrypted += char(data[i] ^ key[i % key.length()]);
  }
  return encrypted;
}

// =====================================================
// STRUCTURED OUTPUT
// =====================================================

void printStructuredOutput() {

  Serial.println("\n[Structured Output]");
  Serial.println("{");

  Serial.print("  \"device_count\": ");
  Serial.println(deviceCount);

  Serial.print("  \"risk_weightage\": ");
  Serial.println(riskWeightage);

  Serial.print("  \"trust_score\": ");
  Serial.println(trustScore);

  Serial.println("}");
}
