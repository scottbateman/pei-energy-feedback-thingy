pei-energy-feedback-thingy
==========================

Description, walkthrough and code for building an energy feedback appliance for Prince Edward Island.

Description and Motivation
--------------------------

Who is this guide for and how should I follow it?
--------------------

Equipment Used
--------------

Installing an OS (Raspbian)
---------------------------

### Updating the Software

You should update always keep your OS and software up to date. Raspbian and all of the software it contains are often updated to take care of any security problems or fix any bugs. To update your Raspbian OS and software, you can run this command at the prompt


Installing Required Software
----------------------------
### Installing a new Wireless Network Manager

I have had a problem with getting the wireless adapter to connect to both my home and the University networks using the default wireless service in Raspbian. The only, and probably the easiest, way to get around this is to install a new wireless networking service called, wicd. To do this just run the following at the command prompt:

```
sudo apt-get update
sudo apt-get install wicd
sudo apt-get install wicd-curses
```

The first install command will provide the basic wicd software and also provide you with a graphical interface for when you are using Raspbian's GUI. The second command will install a command line interface for working with the wicd software. Since, we are working at the command prompt we will use wicd-curses.

You will then need to configure wicd, by typing the following:

```
wicd-curses
```

You will then get and interface that will allow you to *hopefully* select your wireless network:
- use the 'up' and 'down' arrow keys to select it from the list
- press the 'right arrow' key to configure your network
- the main thing you will need to do is to enter your wireless network key (in the line marked *Key*) 
- to have your network connect automatically from now on, select the appropriate line and press space bar to mark the option
- once you have configured you can hit 'F10' key to save
- you will then need to use the arrow keys to select your newly configured wireless network and hit 'enter' to connect 
- you will see status messages that describe your progress in connecting at the bottom of the screen
- when you are connected, you can press Q to quit the wicd-curses interface.

If you get lost at any point here is a good walkthrough to get wicd installed: [http://dembtech.blogspot.ca/2012/09/how-to-install-wifi-on-raspberry-pi.html](A Walkthrough with pictures of setting up wicd)


Wiring up the Lights
--------------------

Writing the Code
----------------

Building an Enclosure
---------------------

The Finished Project
--------------------
