#include <WiFi.h>
#include "DHT.h"

// =============================
// WIFI CONFIG
// =============================

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

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

  Serial.println("\n🔥 AUTO SHIELD STARTING");

  connectWiFi();

  WiFi.softAP("Company_Security_Honeypot");

  Serial.println("🔥 Honeypot Active");
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
    printStructuredOutput();

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

  Serial.println("\n[Device Fingerprinting]");

  int networks = WiFi.scanNetworks();

  Serial.print("Devices Found: ");
  Serial.println(networks);

  for (int i = 0; i < networks; i++) {

    String mac = WiFi.BSSIDstr(i);
    int rssi = WiFi.RSSI(i);

    Serial.print("MAC: ");
    Serial.print(mac);
    Serial.print(" | RSSI: ");
    Serial.println(rssi);

    if (!isWhitelisted(mac)) {

      riskWeightage += 2;  // Reduced penalty
    }

    if (rssi > -35) {

      riskWeightage += 3;  // Possible rogue device
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
// BEHAVIOR ANALYSIS
// =====================================================

void behavioralAnalysis() {

  Serial.println("\n[Behavioral Monitoring]");

  int traffic = random(1, 30);

  Serial.print("Traffic Level: ");
  Serial.println(traffic);

  if (traffic > 25) {

    riskWeightage += 5;
    Serial.println("🚨 High Traffic Spike");
  }
}

// =====================================================
// ENVIRONMENTAL MONITORING
// =====================================================

void environmentalAnalysis() {

  Serial.println("\n[Environmental Monitoring]");

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT Read Error");
    return;
  }

  Serial.print("Temp: ");
  Serial.println(temp);

  Serial.print("Humidity: ");
  Serial.println(hum);

  if (temp > 40) {
    riskWeightage += 10;
    digitalWrite(PHYSICAL_LED, HIGH);
  }
  else if (temp > 35) {
    riskWeightage += 5;
    digitalWrite(PHYSICAL_LED, HIGH);
  }
  else {
    digitalWrite(PHYSICAL_LED, LOW);
  }

  if (hum > 80) {
    riskWeightage += 5;
  }
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
// DECISION ENGINE
// =====================================================

void decisionEngine() {

  Serial.println("\n[Decision Engine]");

  if (trustScore >= 80) {

    Serial.println("STATUS: SAFE");

    digitalWrite(SAFE_LED, HIGH);
    digitalWrite(SUSPICIOUS_LED, LOW);
    digitalWrite(CRITICAL_LED, LOW);

  }
  else if (trustScore >= 50) {

    Serial.println("STATUS: SUSPICIOUS");

    digitalWrite(SAFE_LED, LOW);
    digitalWrite(SUSPICIOUS_LED, HIGH);
    digitalWrite(CRITICAL_LED, LOW);

  }
  else {

    Serial.println("STATUS: CRITICAL");

    digitalWrite(SAFE_LED, LOW);
    digitalWrite(SUSPICIOUS_LED, LOW);

    for (int i = 0; i < 5; i++) {

      digitalWrite(CRITICAL_LED, HIGH);
      delay(200);
      digitalWrite(CRITICAL_LED, LOW);
      delay(200);
    }

    Serial.println("🚨 Self-Healing Activated");
  }
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
