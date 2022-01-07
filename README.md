## LED Strip

### Equipment

I used a Raspberry Pi Zero W, and a 150 LED WS2812b LED strip.
The LED Strip was connected to the Pi at the 5V, GND and GPIO 18 pins, as defined in `strip.py`

### Installation

- Setup a Raspberry Pi with an internet connection and Docker installed
- Clone this repo (`git clone https://github.com/tedbennett/led-strip.git`)
- Change to the led-strip directory `cd led-strip`
- Build the image `docker build -t led-strip .`
- Run the image `docker run --privileged` (the `rpi_ws281x` packaged requires privileged permissions)
