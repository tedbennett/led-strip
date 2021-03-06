# LED Strip

## Equipment

I used a Raspberry Pi Zero W, and a 150 LED WS2812b LED strip.
The LED Strip was connected to the Pi at the 5V, GND and GPIO 18 pins, as defined in `strip.py`

## Installation

- Setup a Raspberry Pi with an internet connection and Docker installed
- Clone this repo (`git clone https://github.com/tedbennett/led-strip.git`)
- Change to the led-strip directory `cd led-strip`
- Build the image `docker build -t led-strip .`
- Run the image `docker run --privileged -p 80:80 led-strip` (the `rpi_ws281x` packaged requires privileged permissions)

## API

### Get LED Config

**Definition**

`GET /api/config`

**Response**

- `200 OK` on success

```json
[
  {
    "colours": ["#FFFFFF", "9EF012", "#000000"],
    "delay": 10
  }
]
```

### Create LED Config

**Definition**

`POST /api/config`

**Response**

- `200 OK` on success

```json
[
  {
    "colours": ["#FFFFFF", "9EF012", "#000000"],
    "delay": 10
  }
]
```
