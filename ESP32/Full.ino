#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

const char *ssid = "arun laptop";
const char *password = "123456789";
const char *serverURL = "http://192.168.137.188:8000/api/rfid/";  // Change this to your actual API endpoint

#define SS_PIN 21    // RC522 Slave Select pin
#define RST_PIN 22   // RC522 Reset pin
#define BUZZER_PIN 25 // Buzzer pin

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
WiFiServer server(80);

const int freq = 2000;    // Buzzer frequency
const int channel = 0;    // PWM channel
const int resolution = 8; // 8-bit resolution

void setup() {
  Serial.begin(115200);
  while (!Serial); // Wait for Serial monitor

  pinMode(BUZZER_PIN, OUTPUT);

  // Initialize SPI and RFID module
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("RFID Scanner Ready. Scan a card...");

  // Configure PWM for the buzzer
  // ledcSetup(channel, freq, resolution);
  // ledcAttachPin(BUZZER_PIN, channel);

  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP: " + WiFi.localIP().toString());
  server.begin();
}

void sendCardUID(String cardUID) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"card_uid\":\"" + cardUID + "\"}";
    int httpResponseCode = http.POST(jsonPayload);

    Serial.print("Server Response Code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
    }

    http.end();
  } else {
    Serial.println("WiFi not connected. Unable to send data.");
  }
}

void loop() {
  // ✅ RFID Card Detection
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String cardUID = "";
    Serial.print("Card UID: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      cardUID += String(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println(cardUID);

    // Send Card UID to Server
    sendCardUID(cardUID);

    // Trigger Buzzer on Card Scan
    tone(BUZZER_PIN, 2000, 200);
    delay(200);
    mfrc522.PICC_HaltA();
    delay(1000);  // Avoid multiple triggers
  }

  // ✅ Web Server Control
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client.");
    String currentLine = "";

    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        
        if (c == '\n') {
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.print("Click <a href=\"/H\">here</a> to turn the Buzzer ON.<br>");
            client.print("Click <a href=\"/L\">here</a> to turn the Buzzer OFF.<br>");
            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }

        // Handle Web Requests
        if (currentLine.endsWith("GET /H")) {
          ledcWrite(channel, 128);  // Activate buzzer
        }
        if (currentLine.endsWith("GET /L")) {
          ledcWrite(channel, 0);  // Turn off buzzer
        }
      }
    }
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
