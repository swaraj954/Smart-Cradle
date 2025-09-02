Realtime_CryDetection detects cries from clips of 10 seconds audio
GUIDesign specifies the layout of the webpage
Backend is responsible for deplaying info on website and enabling actuators or reading data on click of button



To actually run these codes you need to connect the following sensors/actuators to the raspberry 
as follows:


Stepper Motor IN1,IN2,IN3,IN4 to GPIO 14 15 18 23 respectively
Soil sensor to GPIO 21 and ground
RED LED to GPIO 25 and gnd
Buzzer to  GPIO 8 and gnd
USB microphone to port number 2

The file strucutre needs to be as follows(inside of raspberry pi):

Inside /home/sensor:

	Inside python_code folder:
		Realtime_CryDetection.py
		(This file we generate in "Cry Detection Part" Folder)
	
	Inside test Folder:
		backend.py
			inside tempelates folder:
				index.html


Code will not work if file structure not correct

