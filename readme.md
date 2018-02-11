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

		sudo nano /etc/network/interfaces

			# content
			auto lo
			iface lo inet loopback

			auto eth0
			iface eth0 inet dhcp

			auto wlan0
			allow-hotplug wlan0
			iface wlan0 inet dhcp
			wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
			iface default inet dhcp


			sudo systemctl start dhcpcd
			sudo service dhcpcd restart
			systemctl daemon-reload
			systemctl status dhcpcd.service

			sudo dhcpcd -q -d

			wpa_passphrase MYSSID passphrase

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

		# # INSTALL GIT

		# sudo apt-get install libcurl4-openssl-dev
		# sudo apt-get install python-virtualenv python-dev libcurl4-gnutls-dev

		# sudo apt-get install gettext
		# wget https://www.kernel.org/pub/software/scm/git/git-2.3.0.tar.xz
		# tar -xvf git-2.3.0.tar.xz
		# cd git-2.3.0/
		# ./configure --prefix=/usr --with-gitconfig=/etc/gitconfig
		# make
		# sudo make install
		# git --version
		cd && git clone https://github.com/AmedeoSpagnolo/feldman_led_matrix.git
		cd feldman_led_matrix

		sudo locale-gen "en_US.UTF-8"
		sudo dpkg-reconfigure locales

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
		make install

		<!-- rgbmatrix -->
		cd ~/feldman_led_matrix/rpi-rgb-led-matrix-master/bindings/python && python setup.py install

		sudo apt-get update
		sudo apt-get upgrade
		sudo aptitude install libgraphicsmagick++-dev libwebp-dev
		sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
		sudo apt-get install libwebp-dev
		sudo apt-get install python2.7-dev python-pillow -y

		sudo apt-get install python-pip
		python -m pip install Pillow
		# pip install Cython

		sudo pip install requests

[disable integrated sound card](https://www.raspberrypi.org/forums/viewtopic.php?t=18573)
		# sudo leafpad /etc/modprobe.d/alsa-base.conf
		# # comment the line options snd-usb-audio index=-2

## Wiring

Follow the [instuction](https://github.com/AmedeoSpagnolo/feldman_led_matrix/blob/master/wiring.md) for wiring the led Screen
more [info](https://cdn-learn.adafruit.com/assets/assets/000/015/207/medium800/raspberry_pi_wiring_diagram.png?1394711938)

## Run

### Simple Feldman loader

		./loader

###### alternative

		cd ~/feldman_led_matrix/scripts/ && sudo python feldman_loader.py --boris --led-rows=16 --led-chain=2


### Server Felman

		./matrix

###### alternative

		cd ~/feldman_led_matrix/scripts/ && sudo python feldman_server1.py --boris --led-rows=16 --led-chain=2

## Dev

#### Automatic Update

		gulp

https://raspberrypi.stackexchange.com/questions/6757/how-to-use-ssh-out-of-home-network

## TO DO
		no double font
		adjustment letters
		flickering problem
