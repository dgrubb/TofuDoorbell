# TofuDoorbell

This project was requested by a friend who owns a novelty-themed shop, [Tofu Cute](https://www.tofucute.com/), and wants to play an audio clip whenever a customer enters the premises. The implicit requirements are that a computing platform should support audio playback (or trigger audio playback on an external device) and be able to detect input from a physical switching device which can be mounted to a door. Naturally, an Arduino or Raspberry Pi level device spring to mind immediately. 

I opted for a Raspberry Pi as it has the requisite GPIO inputs, a dedicated standard 3.5mm audio output jack (whatever Apple Inc says), and can support a complete OS to take care of file I/O and supply a networking stack. The latter allows for me to make the management experience more pleasant by adding a small webservice to the device which can manage the audio clips and allow them to be swapped out, even though the device will probably be installed headless.

## Hardware Components

* Raspberry Pi 2/3
* Some kind of doorsensor which translates to a logical switch (high/low voltage). For testing I used a simple [door mounted reed switch.](https://www.amazon.com/gp/product/B00HR8CT8E)

## Software Components

The software requirements can be satisfied by creting two simple services which can be launched through systemd:

* doorbell: a Python script which monitors the GPIO for activity and plays back audio according to input triggers. 
* webservice: a NodeJS application which serves up a web-interface for deleting clips and uploading new ones. 

## Requirements

* NodeJS 
* Python
* python-pigpio
