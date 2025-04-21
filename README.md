# Train Object Detection and Crack Detection with IoT (ThingSpeak)

## Overview

This project utilizes a Raspberry Pi and an ultrasonic sensor to measure the distance between the train's wheels and the track. It also uses an IR sensor to detect cracks on the tracks. The distance measurements and crack detection data are sent to ThingSpeak for real-time monitoring.

## Components Used

- **Raspberry Pi 3**: To run the Python code and connect to the sensors.
- **Ultrasonic Sensor (HC-SR04)**: To measure the distance.
- **IR Sensor**: To detect cracks.
- **ESP 01**: Wireless communication.
- **Servo Motor**: To rotate ( connected with ultrasonic sensor).
- **ThingSpeak**: IoT platform to visualize the data.
- **Buzzer**: To buzz when object detected and is near.

## Features

- **Distance Measurement**: Uses an ultrasonic sensor to measure the distance between the train's wheels and the track.
- **Crack Detection**: Uses an IR sensor to detect cracks on the track.
- **Data Sending**: Sends data to ThingSpeak via MQTT, including the distance and crack detection status.
- **Matlab Analysis**: to reduce noice and visualise and gather useful information.
## Hardware Setup and Wiring

### Raspberry Pi Connections:
1. **HC-SR04 Ultrasonic Sensor:**
   - **VCC** -> 5V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **Trig** -> GPIO 23
   - **Echo** -> GPIO 24

2. **HW-201 IR Sensor:**
   - **VCC** -> 5V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **OUT** -> GPIO 17

3. **ESP01 Wi-Fi Module:**
   - **VCC** -> 3.3V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **TX** -> RX on Raspberry Pi (GPIO15)
   - **EN** -> 3.3V on Raspberry Pi
   - **RST** -> 3.3V on Raspberry Pi
   - **RX** -> RX on Raspberry Pi (GPIO14)

4. **Buzzer (if used):**
   - **GND** -> GND on Raspberry Pi (the smaller pin in buzzer)
   - **Control** -> GPIO 26

## 🚀 Setup Instructions

1. **Install Raspberry Pi OS:**
   - Use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash Raspberry Pi OS on the SD card.

2. **Boot & Connect Pi:**
   - Insert the SD card, power on, and connect to network.
   - For headless setup:
     ```bash
     ssh pi@raspberrypi.local
     # Default password: raspberry 
     ```
     (password is not shown on the screen)
3. **Create the Python script:**

   ```bash
      nano mainTrain.py
   ```
Paste your mainTrain.py code.
Save with Ctrl + O, Enter, and exit with Ctrl + X.
4. **Create virtual environment & activate it:**

   ```bash
      sudo apt update
      sudo apt install python3-pip python3-venv
      python3 -m venv mqtt-env
      source mqtt-env/bin/activate
   ```
4. **Install required libraries:**

*Create a requirements.txt:*

   ```bash
      nano requirements.txt
   ```
*Add:*
   ```bash
      RPi.GPIO
      paho-mqtt
      requests
   ```
*Then install:*

   ```bash
      pip install -r requirements.txt
   ```
5. ** Run the Script **
   ```bash
      python3 mainTrain.py
   ```

## 📡 ThingSpeak Setup

1. **Create a free account** on [ThingSpeak](https://thingspeak.com)

2. **Create a new channel** and configure it:
   - **Channel ID:** `enter your channel id` *(replace with your own if necessary)*
   - **Write API Key:** `enter your write api keys`

3. **Add 2 fields** under your channel settings:
   - `Field 1`: Distance (cm)
   - `Field 2`: Crack Detection Status (1 or 0)

4. **(Optional but Recommended)**: Use **MATLAB Visualization** in ThingSpeak to apply Digital Signal Processing (DSP) filters to clean and smooth raw data.

   - Navigate to **Apps > MATLAB Analysis > New**, then write a filter script like:
     ```matlab
     % Read data from channel
     data = thingSpeakRead({enter your channel id}, 'Fields', [1,2], 'NumPoints', 100);
     distance = data(:,1);
     crack = data(:,2);

     % Apply moving average filter to distance
     smoothedDistance = movmean(distance, 5);

     % Plot
     plot(smoothedDistance);
     title('Smoothed Distance using Moving Average');
     ylabel('Distance (cm)');
     xlabel('Time');
     ```
   - Save and run to visualize the filtered sensor data.
   - 
## My Public URL :
https://thingspeak.mathworks.com/apps/matlab_visualizations/617464 - FOR MATLAB VISUALS
https://thingspeak.mathworks.com/channels/2884430 - MY THINGSPEAK CHANNEL
---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
<img width="516" alt="image" src="https://github.com/user-attachments/assets/a72d6076-0ab4-4fe1-be3f-69d9b6654927" /> 
<img width="347" alt="image" src="https://github.com/user-attachments/assets/f5e94588-034d-496a-a2d9-ff2cc3ca9fc6" />
<img width="805" alt="image" src="https://github.com/user-attachments/assets/51bb8725-751b-433c-bfdc-955b9dca2506" />



