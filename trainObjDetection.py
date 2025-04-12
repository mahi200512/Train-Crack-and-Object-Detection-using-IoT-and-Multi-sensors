import RPi.GPIO as GPIO
import time
import numpy as np
import paho.mqtt.client as mqtt

# GPIO Pin Definitions
IR_SENSOR_PIN = 17      # GPIO for Crack Detection (IR Sensor)
TRIG = 23               # GPIO for Ultrasonic Sensor - Trigger
ECHO = 24               # GPIO for Ultrasonic Sensor - Echo

# IoT Configuration (ThingSpeak)
BROKER = "mqtt3.thingspeak.com"
PORT = 1883
CHANNEL_ID = "2884430"         # Replace with your ThingSpeak Channel ID
WRITE_API = "Z6ZZLFVB79612IWW" # Replace with your ThingSpeak API Key

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Moving Average Filter (for DSP)
def moving_average_filter(data, window_size=3):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Function to Measure Distance (Ultrasonic Sensor)
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time, stop_time = time.time(), time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound = 343 m/s
    return distance

# Function to Send Data to IoT Cloud (ThingSpeak)
def send_to_cloud(distance, crack_status):
    topic = f"channels/{CHANNEL_ID}/publish/{WRITE_API}"
    payload = f"field1={distance}&field2={crack_status}"
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    client.publish(topic, payload)
    print(f"Publishing: {payload} to {topic}")
    client.disconnect()

distance_values = []

try:
    while True:
        # Step 1: Crack Detection
        crack_detected = GPIO.input(IR_SENSOR_PIN) == 0  # 0 -> Crack detected

        # Step 2: Object Detection with Distance Measurement
        distance = measure_distance()
        distance_values.append(distance)

        # Step 3: Apply DSP Filtering (Moving Average)
        if len(distance_values) >= 5:
            filtered_distances = moving_average_filter(distance_values, window_size=5)
            smooth_distance = filtered_distances[-1]  # Latest smoothed value
            distance_values.pop(0)  # Maintain a fixed window size
        else:
            smooth_distance = distance

        # Step 4: Send Data to IoT
        send_to_cloud(smooth_distance, 1 if crack_detected else 0)

        # Step 5: Display Real-time Output
        print(f"Distance: {smooth_distance:.2f} cm | Crack Detected: {'YES' if crack_detected else 'NO'}")

        time.sleep(1)  # Adjust delay as needed

except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()
