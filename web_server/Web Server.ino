#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include "oled_u8g2.h"  // OLED Display

const char* ssid = "SmartFactory";               // WIFI ID
const char* password = "inha4885";               // WIFI PW

OLED_U8G2 oled;   // create OLED object
WebServer server(80);   // create WebServer object, port 

int temp_sensor = A2;    // temperature sensor
int Vo;
double R1 = 10000;
double logR2, R2, T, Tc, Tf;
double c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;


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
  Serial.println("main page from ");     // info to access page with serial      

  String clientIP = server.client().remoteIP().toString(); // client's IP address 
  String maskedIP = maskIPAddress(clientIP);

  Vo = analogRead(temp_sensor);         // read from temperature sensing value
  R2 = R1 * (4095.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  Tc = T - 273.15;  //celsius temperature
  Tf = (Tc * 9.0/5.0) + 32.0;

  String message = "It's inha smartfactory webserver\n\n";
  message = message +  "Your IP address: " + maskedIP;
  message = message + "\nTemperature: " + String(Tc) + "C, " + String(Tf) + "F";      
  server.send(200, "text/plain", message); // status code 200(ok) , format, message

  Serial.println(clientIP);
  Serial.print("섭씨온도: ");
  Serial.print(Tc);
  Serial.print("C,  "); 
  Serial.print("화씨온도: ");
  Serial.print(Tf);
  Serial.println("F");
}

String maskIPAddress(String ip_address) {
  String masked_ip;
  
  // IP 주소의 중간 부분 가리기
  int first_dot = ip_address.indexOf('.');
  int second_dot = ip_address.indexOf('.', first_dot + 1);
  
  masked_ip += ip_address.substring(0, first_dot + 1);
  masked_ip += "***";
  masked_ip += ip_address.substring(second_dot);
  
  return masked_ip;
}


