# Train Object Detection and Crack Detection with IoT (ThingSpeak)

## Overview

This project utilizes a Raspberry Pi and an ultrasonic sensor to measure the distance between the train's wheels and the track. It also uses an IR sensor to detect cracks on the tracks. The distance measurements and crack detection data are sent to ThingSpeak for real-time monitoring.

## Components Used

- **Raspberry Pi**: To run the Python code and connect to the sensors.
- **Ultrasonic Sensor (HC-SR04)**: To measure the distance.
- **IR Sensor**: To detect cracks.
- **ThingSpeak**: IoT platform to visualize the data.

## Features

- **Distance Measurement**: Uses an ultrasonic sensor to measure the distance between the train's wheels and the track.
- **Crack Detection**: Uses an IR sensor to detect cracks on the track.
- **Data Sending**: Sends data to ThingSpeak via MQTT, including the distance and crack detection status.

## Hardware Setup and Wiring

### Raspberry Pi Connections:
1. **HC-SR04 Ultrasonic Sensor:**
   - **VCC** -> 5V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **Trig** -> GPIO Pin (e.g., GPIO17)
   - **Echo** -> GPIO Pin (e.g., GPIO27)

2. **HW-201 IR Sensor:**
   - **VCC** -> 5V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **OUT** -> GPIO Pin (e.g., GPIO22)

3. **GY-61 Accelerometer/Gyroscope:**
   - **VCC** -> 3.3V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **SDA** -> GPIO Pin (e.g., GPIO2)
   - **SCL** -> GPIO Pin (e.g., GPIO3)

4. **ESP8266 Wi-Fi Module:**
   - **VCC** -> 3.3V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **TX** -> RX on Raspberry Pi (GPIO15)
   - **RX** -> TX on Raspberry Pi (GPIO14)

5. **Micro Servo Motor (if used):**
   - **VCC** -> 5V on Raspberry Pi
   - **GND** -> GND on Raspberry Pi
   - **Control** -> GPIO Pin (e.g., GPIO18)

## Installation Instructions

### Step 1: Install Dependencies

1. Ensure your Raspberry Pi is running a supported version of Raspbian.
2. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/TrainProject.git
    cd TrainProject
    ```

3. Install the required Python libraries:
    ```bash
    sudo apt update
    sudo apt install python3-pip
    pip3 install -r requirements.txt
    ```

4. Make sure the GPIO pins are set up correctly in the script (`trainObjDetection.py`).

### Step 2: Run the Code

1. Start the script:
    ```bash
    python3 trainObjDetection.py
    ```

2. The script will continuously measure the distance, check for cracks, and send the data to ThingSpeak.

### Step 3: Monitor the Data on ThingSpeak

1. Go to your ThingSpeak channel dashboard to view the data.
   - URL: [https://thingspeak.com](https://thingspeak.com)
   - Channel ID: `2884430` (replace with your own channel ID if necessary).
   - API Key: Use your ThingSpeak write API key.

## How It Works

- The script first measures the distance using the ultrasonic sensor.
- It then checks for cracks using the IR sensor.
- The data (distance and crack detection status) is sent to ThingSpeak via MQTT.
- The script runs in a loop, continuously measuring and sending data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
![Screenshot 2025-03-06 122654](https://github.com/user-attachments/assets/7a4a9b91-12b9-4330-9129-f0fd7908dbe8)
