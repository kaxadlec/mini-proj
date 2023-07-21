#include "oled_u8g2.h" // Include the library for OLED control
#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>

const char* ssid = "iptime_501";  // WIFI ID
const char* password = "11238591";  // WIFI PW

OLED_U8G2 oled; // Create an OLED object
WebServer server(80);  // Create a web server object

//-------------------------------------------------------------------------------------------
// ETBoard pin number settings, related variables
//-----------------------------------------------------------------------------------------
int leds[] = {D2, D3, D4, D5}; // LED pin number array (red, blue, green, yellow)
int num_leds = 4;              // Number of LEDs
int red_button = D6;            
int blue_button = D7;
int photoresister_sensor = A1; // Photoresistor sensor
int temperature_sensor = A2;   // Temperature sensor
// Variables for calculating the current temperature
int Vo;
double R1 = 10000;
double logR2, R2, T, Tc, Tf;
double c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
int trig_pin = D9;      // TRIG pin setting (ultrasonic transmitter pin)
int echo_pin = D8;      // ECHO pin setting (ultrasonic receiver pin)
int count;      // Counter variable
int pre_time = 0;   // Previous time when an object passed by
int sensor_value;   // Photoresister sensor value
String factory_status = "Stopped";

void setupLEDs() { // Set all LED pins to OUTPUT mode
  for (int i = 0; i < num_leds; i++) {
    pinMode(leds[i], OUTPUT); 
  }
}

void setupButtons(){  // Set red, blue button pins to INPUT mode
  pinMode(red_button, INPUT);
  pinMode(blue_button, INPUT); 
}
void setupUltrasonics() { // Ultrasonic pin setup
  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);
}

void setupWiFi() {
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
  Serial.println(WiFi.localIP()); // Print assigned IP address when it connected
}

void setup() {
  Serial.begin(115200); // Serial communication speed of the ET board
  setupLEDs(); // Call LED setup function
  setupButtons(); // Call Button setup function
  setupUltrasonics(); // Call ultrasonic pin setup function
  oled.setup();
  setupWiFi(); // Call Wi-Fi setup function

  server.on("/", handleRootEvent);  // Set the root URL to call the handleRootEvent function
  server.begin();
  Serial.println("WEB server started");   
} 

void loop() {
  controlFactoryStatus();
  controlLEDs(); // Call LED control function
  readPhotoResister(); // Call photoresistor measurement function
  readTemperature(); // Call temperature measurement function
  updateCountAndDistance(); // Call object recognition count function       
  displayOLED();  // Call OLED display function 

  server.handleClient(); // Process incoming client requests
  delay(2);
}

void controlLEDs() {  // LED control function

}

void readPhotoResister(){ // Photoresistor measurement function
  sensor_value = analogRead(photoresister_sensor);   // Save the value measured by the photoresistor sensor
} 

void readTemperature() { // Temperature measurement function and conversion to Celsius and Fahrenheit
  int Vo = analogRead(temperature_sensor); // Read the value from the temperature sensor and convert to temperature
  R2 = R1 * (4095.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2));
  Tc = T - 273.15;
  Tf = (Tc * 9.0/5.0) + 32.0;
}

void updateCountAndDistance() { // Count objects recognized through the ultrasonic sensor
    if (factory_status == "Running") {
    long duration, distance;
    digitalWrite(trig_pin, LOW);                
    delayMicroseconds(2);
    digitalWrite(trig_pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig_pin, LOW);                

    duration = pulseIn (echo_pin, HIGH);        
    distance = ((34 * duration) / 1000) / 2;    

    if (distance > 2 && distance < 5)            
    {
        int now_time = millis();
        if (now_time - pre_time > 500)           
        {
            count += 1;                         
            pre_time = now_time;                
        }
    }
  }
  resetButtonCheck();  // Call reset button function
}

void resetButtonCheck() { // Reset button function (resetting the count variable here)
  if (digitalRead(red_button) == LOW) {
    //Serial.println("count reset");
    count = 0;
  }
}

void displayOLED() {  // OLED display function
  char text1[32] = "count : ";
  char value1[32];
  String str1 = String(count, DEC);
  str1.toCharArray(value1, 6);
  strcat(text1, value1);

  char factoryStatus[8];
  if (factory_status == "Stopped") {
    strcpy(factoryStatus, "Stopped");
  } else {
    strcpy(factoryStatus, "Running");
  }

  oled.setLine(1, "*Smart Factory");
  oled.setLine(2, text1);
  oled.setLine(3, factoryStatus);
  oled.display();
}

void controlFactoryStatus() {
  if (digitalRead(red_button) == LOW) {
    Serial.println("Factory Status set to Stopped");
    factory_status = "Stopped";
  }

  if (digitalRead(blue_button) == LOW) {
    Serial.println("Factory Status set to Running");
    factory_status = "Running";
  }
}

void handleRootEvent() {           // Function for handling root URL access
  Serial.println("Main page from ");     // Print info about accessing the page through serial
  String clientIP = server.client().remoteIP().toString();  // Get client's IP address
  String maskedIP = maskIPAddress(clientIP);    // Mask a portion of the client's IP address

  if (factory_status == "Running") { // Only gather data if factory_status is "Running"
    readTemperature(); // Call temperature measurement function
    readPhotoResister(); // Call photoresister measurement function
    updateCountAndDistance(); // Call object count function
  }

  String message = "HyeonJin SmartFactory WebServer\n";
  message += "---------------------------------\n";
  message += "Factory Status: " + factory_status + "\n";
  message += "Your IP address: " + maskedIP + "\n";
  if (factory_status == "Running") {
    message += "\nTemperature: " + String(Tc) + "C/" + String(Tf) + "F";  
    message += "\nPhotoresistor Value: " + String(sensor_value);
    message += "\nObject Count: " + String(count);
  }

  server.send(200, "text/plain", message); // Status code 200 (OK), format, message
  Serial.println(message); // Monitoring
}

String maskIPAddress(String ip_address) {
  String masked_ip;

  // Replace portions of the IP address excluding the beginning and end with ***
  int first_dot = ip_address.indexOf('.');
  int last_dot = ip_address.lastIndexOf('.');

  masked_ip += ip_address.substring(0, first_dot + 1);
  masked_ip += "***.***";
  masked_ip += ip_address.substring(last_dot);

  return masked_ip;
}
