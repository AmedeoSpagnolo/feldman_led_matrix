## Setup RaspberryPi

1) Download
[latest raspbian lite OS](https://downloads.raspberrypi.org/raspbian_lite_latest).

2) Install the operative system image on the SD card following the [instructions](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md).

3) Connect RaspberryPi to power

4) Connect RaspberryPi to internet with a LAN cable

5) Connect a monitor(HDMI), keyboard(USB) and mouse(USB)

5) Open terminal and change password (any problem? [instruction](https://www.raspberrypi.org/documentation/linux/usage/users.md))

		passwd
		# follow instruction

6) Enable SSH on RaspberryPi [instruction](https://www.raspberrypi.org/documentation/remote-access/ssh/)

		sudo raspi-config
		# Select: Interfacing Options
		# Select: SSH
		# Choose: YES / OK / Finish

7) Connect RaspberryPi Wifi Automatically

		sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

		# content:

		country=GB
		ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
		update_config=1

		network={
        	ssid="<SSID_name>"
        	scan_ssid=1
        	psk="<password>"
		}

8) run:

	sudo halt

9) Disconnect monitor, keyboard and mouse

## Connect to RasberryPi

1) Connect your computer on the same network

2) Find RasberryPi IP

		nmap -sP $(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' | head -n 1 | cut -d. -f1 -f2 -f3).0/24

alternative:

		# find you IP (example 192.168.1.52)
		ifconfig
		# scan network
		nmap -sP 192.168.1.0/24

4) connect SSH to RaspberryPi with the command

		ssh pi@<raspberrypi_IP>
		# example:
		#	ssh pi@192.168.1.52

alternative:

		ssh -i ~/.ssh/id_rsa.pub pi@<raspberrypi_IP>
		# your id_rsa.pub needs to be in ~/.ssh/authorized_keys on RaspberryPi

## Setup

1) On RaspberryPi download github repositorie

		cd && git clone https://github.com/AmedeoSpagnolo/feldman_led_matrix.git
		cd feldman_led_matrix

9) Setup

		# install python library rgbmatrix
		cd ~/feldman_led_matrix
		wget https://github.com/hzeller/rpi-rgb-led-matrix/archive/master.zip
		unzip master.zip
		rm master.zip
		cd rpi-rgb-led-matrix-master/
		make
		cd /bindings/python
		make

		# Pillow
		python -m pip install Pillow

## Wiring

Follow the [instuction](http://google.com) for wiring the led Screen

## Run

### Simple Feldman loader

		cd ~/feldman_led_matrix/scripts/ && sudo python feldman_loader.py --led-rows=16 --led-chain=2

### Server Felman

		boris server --led-chain=4 --led-rows=16
		cd ~/feldman_led_matrix/scripts/ && sudo python feldman_server1.py --led-rows=16 --led-chain=2
