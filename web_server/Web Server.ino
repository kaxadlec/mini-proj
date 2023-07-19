#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>

const char* ssid = "SmartFactory";               // WIFI ID
const char* password = "inha4885";               // WIFI PW

// create WebServer object, port
WebServer server(80);                


void setup(void) {
  Serial.begin(115200);   // ESP32 baud rate 
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
  server.handleClient();   // clients process
  delay(2);
}

void handleRootEvent() {           // function to access through root                   
  Serial.println("main page");     // info to access page with serial            
  server.send(200, "text/plain", "It's SmartFactory WEBSERVER"); // status code 200(ok) , format, message
}




