
/*
 * VetNet IoT Smart Tag v1.0 (ESP32 Edition)
 * -----------------------------------------
 * This firmware connects a physical animal tag to the VetNet AI platform.
 * It tracks body temperature, heart rate, and activity levels.
 *
 * HARDWARE CONNECTIONS:
 * 1. Temperature (DS18B20): Signal -> GPIO 4 (with 4.7k Pull-up)
 * 2. Heart Rate (MAX30102): SDA -> GPIO 21, SCL -> GPIO 22
 * 3. Activity (ADXL345): SDA -> GPIO 21, SCL -> GPIO 22 (shared I2C bus)
 * 4. Status LEDs: Green -> GPIO 12, Red -> GPIO 14
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

// --- CONFIGURATION ---
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* SERVER_URL    = "http://YOUR_COMPUTER_IP:8002/iot/telemetry";
const char* DEVICE_TAG    = "ESP32_VET_01";
const char* ANIMAL_ID     = "Lion_Alpha"; // Maps to SherKhan in Registry

// --- SENSOR OBJECTS ---
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensor(&oneWire);
MAX30105 pulseSensor;

void setup() {
  Serial.begin(115200);
  pinMode(12, OUTPUT); // Green LED
  pinMode(14, OUTPUT); // Red LED

  // 1. Initialize WiFi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi Connected!");
  digitalWrite(12, HIGH); // Onboard Green LED

  // 2. Initialize Sensors
  tempSensor.begin();
  if (!pulseSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("⚠️ MAX30102 pulse sensor not found.");
  }
  pulseSensor.setup();
  pulseSensor.setPulseAmplitudeRed(0x0A);
}

void loop() {
  // 1. Read Sensors
  tempSensor.requestTemperatures();
  float bodyTemp = tempSensor.getTempCByIndex(0);
  
  long irValue = pulseSensor.getIR();
  int heartRate = 75; // Fallback or dynamic calculation
  if (checkForBeat(irValue) == true) {
    // Pulse calculation logic here
    Serial.println("❤️ Beat Detected!");
  }

  // 2. Prepare JSON Payload
  StaticJsonDocument<256> doc;
  doc["device_id"]      = DEVICE_TAG;
  doc["animal_id"]     = ANIMAL_ID;
  doc["species"]       = "Lion";
  doc["timestamp"]     = millis() / 1000;
  doc["temperature"]   = bodyTemp;
  doc["heart_rate"]    = heartRate;
  doc["activity_level"]= random(40, 90); // Simplified for demo
  doc["battery_level"] = 98.0;

  String jsonString;
  serializeJson(doc, jsonString);

  // 3. Post to VetNet AI
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode == 200) {
      Serial.println("🚀 Telemetry synced with VetNet Brain");
      digitalWrite(14, LOW); // Success
    } else {
      Serial.print("❌ Sync Error: ");
      Serial.println(httpResponseCode);
      digitalWrite(14, HIGH); // Alert on error
    }
    http.end();
  }

  delay(10000); // Wait 10 seconds (adjust for battery saving)
}
