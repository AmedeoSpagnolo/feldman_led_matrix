### run local server (from other device in the same network)

    cd ~/feldman_led_matrix/frontend && python start_local_server.py

##### simple api request

    curl http://<ip>:<port>

### start simple feldman loader

    cd ~/feldman_led_matrix/scripts && sudo python feldman.py --led-chain=2 --led-rows=16

### start feldman loader with api

    cd ~/feldman_led_matrix/scripts && sudo python feldman.py --api --port=8080 --ip=192.168.50.61 --led-chain=2 --led-rows=16

#### to do
- font
- timing
- animation (prev word)
