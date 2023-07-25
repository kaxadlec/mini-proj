# Smart Factory Kit: Real-time Process Monitoring System Implementation

## Introduction
This project demonstrates the implementation of a real-time process monitoring system using a smart factory kit. The system enables users to monitor, control, and improve the overall efficiency of a factory floor. It displays sensor data on an OLED screen and a GUI application that updates every second. The system is built around an ESP32 microcontroller and uses a combination of Arduino and Python's tkinter libraries to display real-time factory floor conditions on the user's PC. 

### Key Features:
1. Displays factory running state (running or stopped)
2. Monitors internal and external temperature
3. Measures the number of detected objects
4. Displays client IP address
5. Continuously updates the display on an OLED screen and a GUI application
<br/><br/>
## Technical Specifications
### Hardware
- ESP32 microcontroller
- OLED screen
- Multiple sensors:
    - Temperature sensor (analog input)
    - Photoresistor for light level detection (analog input)
    - Ultrasonic sensor for object detection (digital input/output)
### Software
- Arduino IDE for building and uploading code to the ESP32
- ESP32 UART driver for serial communication
- Python's tkinter library for building the GUI application
- Requests library for HTTP connection


### Dependencies
- Arduino libraries
    - WiFi.h
    - WiFiClient.h
    - WebServer.h
<br/><br/>
- Python libraries
    - tkinter
    - requests
    - datetime
    - json
------------------------------------
## How it works
The ESP32 microcontroller collects data from all the attached sensors and sends it to the GUI application built with Python's tkinter. The data includes factory status, internal and external temperature, photoresistor sensor data, object count, and client IP address. The tkinter application displays the collected data on the user's computer screen, updating the values every second. The user can also start or stop the factory and reset the object count using buttons on the GUI application. The system uses the ESP32 Wi-Fi capabilities to connect to a local network and run a web server. The Arduino code handles incoming requests and serves an HTML page with the sensor data. In this real-time process monitoring system implementation, the Arduino and Python code work together to provide a seamless interface for monitoring and controlling the factory floor conditions.
