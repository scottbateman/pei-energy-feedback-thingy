The Prince Edward Island Energy Feedback Appliance (pei-energy-feedback-thingy)
========================================================================

Description, walkthrough and code for building an energy feedback appliance for Prince Edward Island. 

The code in this repository and the README file you are currently reading are designed to guide the development of a simple, low-cost energy feedback appliance. The appliance described in this guide is an easy-to-build and low-cost system that aims to help people become aware of the sources of electricity they are currently using and allow them to adjust their daily consumption practices based on this information.

Motivation
--------------------------
Prince Edward Island (http://www.gov.pe.ca) has three sources of electricity: nuclear generated (imported from New Brunswick), wind-generated (from on-Island turbines), and a diesel generator (used to meet demand when the previous two sources cannot meet demand). The problem is that there is only a fixed amount of reliable electricity that makes up the majority of electricity used on Prince Edward Island (from nuclear). The capacity of the cables from New Brunswick is 200 MW [1], however, the peak demand on the Island reached an all-time high of 252 MW [2]. This means that wind and the diesel generator must make up the difference between. However, wind is a periodic energy source and cannot always make up the difference between the demand and imported electricity. The diesel generator is in place to meet the remainder of the demand. However, the cost of maintaining the fossil fuel generator is extremely high, fossil fuel is increasingly expensive, and when the generator is turned on it releases a considerable amount of air polution. In addition, in 2014, there was a failure to meet the peak demand and a rolling blackout was put in place to avoid a total blackout [3].

This encouraged us to consider consumer devices that might allow people to have a better idea of when and they can adjust there energy consumption behaviour during critical times on the Island, and perhaps even to target their high-energy consumption activities (e.g., using the dishwasher, the clothes dryer, etc.) when overall demand is low, and energy from "clean" sources is high (i.e., wind generated). There exist several consumer devices that allow people to improve their energy consumption based on receiving feedbak at the household level, and, in some cases, allowing for comparing consumption with houses of similar sizes, houses near by, or with personal history. However, rather than a focus on providing feedback on an individual household's consumption, this appliance is designed to provide feedback on "green" and "dirty" energy sources as in a particular region, in this case the provice of Prince Edward Island in Canada (http://www.gov.pe.ca).



Who is this guide for and how should I follow it?
--------------------

Equipment Used
--------------

Installing an OS (Raspbian) on the Raspberry Pi
---------------------------

### Updating the Software

You should update always keep your OS and software up to date. Raspbian and all of the software it contains are often updated to take care of any security problems or fix any bugs. To update your Raspbian OS and software, you can run this command at the prompt


Installing Required Software
----------------------------
### Installing a new Wireless Network Manager

I have had a problem with getting the wireless adapter to connect to both my home and the University networks using the default wireless service in Raspbian. The only, and probably the easiest, way to get around this is to install a new wireless networking service called, wicd. To do this just run the following at the command prompt:

```bash
sudo apt-get update
sudo apt-get install wicd
sudo apt-get install wicd-curses
```

The first install command will provide the basic wicd software and also provide you with a graphical interface for when you are using Raspbian's GUI. The second command will install a command line interface for working with the wicd software. Since, we are working at the command prompt we will use wicd-curses.

You will then need to configure wicd, by typing the following:

```bash
wicd-curses
```

You will then get and interface that will allow you to select your wireless network:
- use the 'up' and 'down' arrow keys to select it from the list
- press the 'right arrow' key to configure your network
- the main thing you will need to do is to enter your wireless network key (in the line marked *Key*) 
- to have your network connect automatically from now on, select the appropriate line and press space bar to mark the option
- once you have configured you can hit 'F10' key to save
- you will then need to use the arrow keys to select your newly configured wireless network and hit 'enter' to connect 
- you will see status messages that describe your progress in connecting at the bottom of the screen
- when you are connected, you can press Q to quit the wicd-curses interface.

If you get lost at any point here is a good walkthrough to get wicd installed: [http://dembtech.blogspot.ca/2012/09/how-to-install-wifi-on-raspberry-pi.html](A Walkthrough with pictures of setting up wicd)

### Configuring Python
To be ablea to get information from the Web about current power production and consumption, we will use Python. Python comes pre-installed with Raspbian, but it does not yet know how to talk to the LEDs we will be wiring to the Pi to provide our visual feedback. We simply need to add a few libraries to make this possible:
```bash
sudo apt-get update
sudo apt-get install python-dev
sudo apt-get install python-rpi.gpio
```


Wiring up the Lights
--------------------

Writing the Code
----------------

Building an Enclosure
---------------------

The Finished Project
--------------------

References
--------------------
[1] http://ruk.ca/content/one-year-pei-electricity 
[2] http://ruk.ca/content/new-pei-electricity-peak-load
[3] http://www.cbc.ca/news/canada/nova-scotia/blizzard-weakens-in-maritimes-moves-on-to-newfoundland-1.2482482
