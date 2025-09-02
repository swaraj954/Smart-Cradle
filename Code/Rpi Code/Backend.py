from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)


STEP_PINS = [14, 15, 18, 23]  
MOISTURE_SENSOR_PIN = 21      
BUZZER_PIN = 8               
LED_PIN = 25                 

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)


for pin in STEP_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)


step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]


swing_direction = 1  


def rotate_stepper(steps, delay=0.005, direction=1):
    steps = abs(steps)
    sequence = step_sequence if direction == 1 else step_sequence[::-1]
    
    for _ in range(steps):
        for step in sequence:
            for pin in range(4):
                GPIO.output(STEP_PINS[pin], step[pin])
            time.sleep(delay)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/swing', methods=['POST'])
def swing_control():
    global swing_direction
    data = request.json

    if data['action'] == 'start':
        # Rotate 180 degrees in the current direction
        rotate_stepper(256, delay=0.005, direction=swing_direction)
        
        # Toggle direction for next swing
        swing_direction *= -1
        return jsonify({"status": "Swing started"})
    elif data['action'] == 'stop':
        return jsonify({"status": "Swing stopped"})
    return jsonify({"status": "Invalid command"}), 400


@app.route('/moisture-status', methods=['GET'])
def check_moisture():
    moisture_detected = GPIO.input(MOISTURE_SENSOR_PIN)
    if moisture_detected == GPIO.LOW:  
        
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        GPIO.output(LED_PIN, GPIO.HIGH)
        return jsonify({"status": "Moisture detected"})
    else:
        
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.output(LED_PIN, GPIO.LOW)
        return jsonify({"status": "No moisture detected"})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()
    while True:
        print("ENTERED")
        check_moisture()

