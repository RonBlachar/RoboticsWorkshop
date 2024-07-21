# User’s manual
## Purpose
The primary purpose of this project is to enable a jeep to navigate to a destination safely without colliding with any obstacles. Using the capabilities of a drone, the system provides a secure and efficient path for the jeep, ensuring it reaches its goal without incident.
## Use
### The Scene
Starting Point: One of the boundaries
Red Boundaries: Define the limits of the area
Black Obstacles: Represent obstacles within the area
Blue Destination: Marks the target location
### Operational Steps
The drone ascends above the scene to gain a clear view
Once stable, the drone captures a photograph of the area
The captured image is processed using a bird's-eye algorithm
The system calculates the optimal route from the starting point to the destination
The calculated route is then translated into specific directions compatible with the jeep’s API
The jeep moves from the starting point to the destination following the calculated path
## Installation Guide
Make sure you have a stable internet connection to prevent communication errors, as we have experienced issues in this area before.
### Devices Required
An Android phone
Another phone (e.g., iPhone)
A laptop
Drone: DJI Mini 3
Drone remote
Jeep robot: Robomaster S1
### Software Requirements
Python packages: Install necessary packages via pip install -r requirements.txt
Android application: Install the required app on the Android phone
Installation Steps
Clone the repository
Github repository
Install the Android App
Follow the instructions in this YouTube video to install the app on your Android phone.
Install the Robomaster App
Download and install the Robomaster app on the second phone via the App Store.
Set Up a Router Using a Personal Phone
Create a mobile hotspot on your personal phone.
Connect the following devices to this hotspot:
The Android phone
The iPhone
The laptop
Connect the iPhone to the Robomaster Jeep
Follow the in-app guide within the Robomaster application to pair the iPhone with the jeep.
Connect the Android phone to the drone remote
Allows our server to remotely control the drone
Run the program
Within the Android app:
 click Takeoff
Using the following commend: python3 main.py
Or by clicking the “Run” button
Error: in case of an error while controlling the drone, click “Disable virtual stick” button in the android app - it allows the operator to manually control the drone and land it safely
You're Good to Go!
Once all devices are connected and the apps are installed, your system is ready to operate.

