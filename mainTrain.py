import RPi.GPIO as GPIO
import time
import requests

# DSP filter
def moving_average(data, window_size=5):
    if len(data) < window_size:
        return sum(data) / len(data)
    return sum(data[-window_size:]) / window_size

# GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# IR Sensor
IR_PIN = 17
GPIO.setup(IR_PIN, GPIO.IN)

# Ultrasonic
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Servo Motor
SERVO = 18
GPIO.setup(SERVO, GPIO.OUT)
pwm = GPIO.PWM(SERVO, 50)  # 50Hz PWM frequency
pwm.start(0)

# Buzzer
BUZZER = 26
GPIO.setup(BUZZER, GPIO.OUT)

# ThingSpeak
THINGSPEAK_URL = "https://api.thingspeak.com/update"
API_KEY = "YOUR_API_KEY_HERE"  # 🔁 Replace with yours

# Buffer for DSP
ultra_data = []

# Set servo angle
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.05)
    GPIO.output(SERVO, False)
    pwm.ChangeDutyCycle(0)

# Measure distance
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.01)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start, stop = time.time(), time.time()
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()

    duration = stop - start
    distance = round(duration * 17150, 2)  # in cm
    return distance

# Buzzer buzz
def buzz():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(BUZZER, GPIO.LOW)

# Main loop
try:
    direction = 1  # 1 for forward, -1 for reverse
    angle = 0

    while True:
        # 1️⃣ Check for crack
        if GPIO.input(IR_PIN) == 0:
            print("🚨 Crack Detected!")
            buzz()

        # 2️⃣ Servo sweep
        set_angle(angle)
        distance = measure_distance()
        ultra_data.append(distance)

        # 3️⃣ DSP filter
        filtered = moving_average(ultra_data, 5)
        print(f"Angle {angle}° | Raw: {distance} cm | Filtered: {filtered:.2f} cm")

        # 4️⃣ Check object presence
        if filtered < 20:
            print("⚠️ Object Detected!")
            buzz()

        # 5️⃣ Send to ThingSpeak
        payload = {
            'api_key': API_KEY,
            'field1': distance,
            'field2': filtered
        }

        try:
            r = requests.get(THINGSPEAK_URL, params=payload)
            print(f"✅ Sent to ThingSpeak | Status: {r.status_code}")
        except Exception as e:
            print("❌ Error sending to ThingSpeak:", e)

        # 6️⃣ Log locally
        with open("log.csv", "a") as f:
            f.write(f"{angle},{distance},{filtered}\n")

        # Update servo angle
        angle += 30 * direction
        if angle >= 180 or angle <= 0:
            direction *= -1  # Reverse direction

        time.sleep(1)  # ~1s per step (ThingSpeak free plan = 15s min interval if frequent, buffer if needed)

except KeyboardInterrupt:
    print("🛑 Interrupted by user. Cleaning up.")
    pwm.stop()
    GPIO.cleanup()
