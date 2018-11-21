# Munchies Robot Hack Demo

Demo and tutorial for https://2018.hackjunction.com/challenges/munchies-robot-hack

## Operating Dobot Magician

### Getting started

* Download Dobot Studio: https://www.dobot.cc/downloadcenter.html
* If you are using Mac, Dobot Studio is by default set to Simplified Chinese. Change the language to English on the top row

* Connect to the robot by plugging in the cable to your computer
* Test the connection with manually commanding the robot to move on Dobot Studio
* Connect to the linear rail by clicking on the icon on Dobot Studio
* Make the robot move to it's default position by pressing "Home"
* On Dobot Studio, go to "Scripts", open the template script "Example_PTP" (downloaded on install) and run it



### Dobot DLL

It is hard to install additional libraries in the Dobot Studio environment. If you want to use additional packages, it might be easier to operate Dobot from outside the Dobot Studio environment.

In order to program Dobot in Python, do the following

* Download DobotDemo v2.0 from https://www.dobot.cc/downloadcenter.html?sub_cat=72#sub-download
* Find the location where your Python is installed (e.g. "C:\Users\username\AppData\Local\Continuum\anaconda3")
* Copy the files in "DobotDemoV2.0\DobotDll\Precompiled\Windows\x64\DobotDll" (e.g. "C:\Users\username\Downloads\DobotDemoV2.0\DobotDll\Precompiled\Windows\x64\DobotDll") to where python is installed
* Test with running DobotControl.py
* Copy the file DobotDllType.py in the folder where you want to program python

### Programming Dobot

Dobot API can be found here: http://www.dobot.it/wp-content/uploads/2018/03/dobot-api-en.pdf
The API is in C, but Dobot supports other programming languages too. List of possible functions can be found on the left sidebar of "Scripts" on Dobot Studio.

Feel free to refer to demo.py about usage!


## Operating GoPro Hero 4

### Getting started
* Install the goprocam library: https://pypi.org/project/goprocam/
* Switch the camera on
* You can communicate the camera remotely via WiFi. First, WiFi must be turned on: go to Setup -> Wireless and press the WiFi icon
* Connect your computer to the WiFi goprohero4 (password: goprohero4)
* Download and run test script gopro_example.py from this repository
