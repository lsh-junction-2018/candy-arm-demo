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

Feel free to refer to examle scripts about usage!

### Example solution description

Our solution moves the robot arm based on coordinates we want the robot hand to go to. However, we have modified the robot end effector by turning it 90 degrees so that we can use the rotation motor coming with the suction cup to rotate the candy scoop (the suction cup is removed).


## Operating GoPro Hero 4

### Getting started
* Install the goprocam library: https://pypi.org/project/goprocam/
* Switch the camera on
* You can communicate the camera remotely via WiFi. First, WiFi must be turned on: go to Setup -> Wireless and press the WiFi icon
* Connect your computer to the WiFi goprohero4
* Download and run test script gopro_example.py from this repository. This script takes a picture and downloads it in the folder you run the script from
* Note that the GoPro WiFi hotspot does not provide internet access. If you need internet when you are operating GoPro, you need to find another internet source than WiFi (such as sharing internet from your phone via USB)

### Example solution description

In our solution, when the script reaches the message that it should look for a candy, it will take a picture of what is in front of the robot. It downloads the picture to the computer and gives some labels of what is seen in the picture. We leave the rest to you!

## Extra

### Candy image dataset

We thought you might want to have a look at image classification possibilities and have thus provided you a small dataset of with pictures of 6 different kinds of candies for toying around. The dataset has around 300 pictures of each candy type divided in folders accordingly (with pictures of the candies on a plate and in a candy box in the shop separated). Even though the dataset is small we hope that this can help you to get started with image classification. You can find it on Google Drive:

https://drive.google.com/open?id=1FsbVszozyPm9nYFP_vNVBO5vsoBYvTld
