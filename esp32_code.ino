#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> 
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10
#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme; // I2C
//Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK); // software SPI

unsigned long delayTime;

const char* ssid = "Mongol"; 
const char* password = "Zvside19";

// ENDPOINT
const char* serverName = "http://192.168.1.67:5001/api/weather/post";

void sendData(float t, float h, float p) {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Tworzenie JSON-a
    StaticJsonDocument<200> doc;
    doc["temp"] = t;
    doc["hum"] = h;
    doc["press"] = p;

    String jsonResponse;
    serializeJson(doc, jsonResponse);

    // Wysłanie POST
    int httpResponseCode = http.POST(jsonResponse);
    
    if (httpResponseCode > 0) {
      Serial.print("Success: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("sending error: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  Wire.begin();

  // WIFI 
  WiFi.begin(ssid, password);
  Serial.print("Łączenie z WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("Connected WiFi!");
  Serial.print("IP ESP32: ");
  Serial.println(WiFi.localIP());

  // 0x77 or 0x76 
  unsigned status;
  status = bme.begin(0x76);  
}

void loop() {
  // put your main code here, to run repeatedly:
  float temp = bme.readTemperature();
  float hum = bme.readHumidity();
  float press = bme.readPressure() / 100.0F;

  Serial.println("Sending Data...");
  sendData(temp, hum, press);

  delay(10000);
}
