#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include "oled_u8g2.h"  // OLED Display

const char* ssid = "SmartFactory";               // WIFI ID
const char* password = "inha4885";               // WIFI PW

OLED_U8G2 oled;   // create OLED object
WebServer server(80);              // create WebServer object, port 


void setup(void) {
  Serial.begin(115200);   // ESP32 baud rate 
  oled.setup();
  WiFi.mode(WIFI_STA);    // Set connection mode
  WiFi.begin(ssid, password);  // try to access WIFI
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {  // wait for connection 
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());   // print assigned IP address when it connected

  server.on("/", handleRootEvent);  // (root, event handling function);

  server.begin();                              
  Serial.println("WEB server started");
}


void loop(void) {
  oled.setLine(1, "inha univ");          // OLED 첫 번째 줄 : 시스템 이름
  oled.setLine(2, "web server");                     // OLED 두 번째 줄 : count 값
  oled.setLine(3, "---------------------");   // OLED 세 번째 줄 
  oled.display();

  server.handleClient();   // clients process
  delay(2);
}


void handleRootEvent() {           // function to access through root                   
  Serial.println("main page");     // info to access page with serial            
  server.send(200, "text/plain", "It's SmartFactory WEBSERVER"); // status code 200(ok) , format, message
}


