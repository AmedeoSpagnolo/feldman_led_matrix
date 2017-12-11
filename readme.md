1) Download
[latest raspbian lite OS](https://downloads.raspberrypi.org/raspbian_lite_latest).

2) Install the operative system image on the SD card following the [instructions](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md).<br>
(I suggest using only the command line without additional programs)

3) Connect RaspberryPi to power 

4) Connect RaspberryPi to internet with a LAN cable

5) Connect your computer on the same network and find your IP using this command in the terminal

		ifconfig | grep 192

6) from your computer search RasberryPi's IP with the command
		
		nmap -sP 192.168.1.0/24

7) connect SSH to RaspberryPi with the command 
		
		ssh pi@192.168.1.<?>

8) Download github repositorie

		git clone <amedeo github repo>
		
9) Install dependecies
		
		sudo atp-get dinstall tree
		...

10) follow the [instuction](http://google.com) for wiring the led Screen

11) start boris loader 
		
		boris loader --led-chain=4 --led-rows=16
		
		
### TO DO
- enable ssh on rasberrypi
 