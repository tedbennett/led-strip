from typing import List, Tuple
import time
from rpi_ws281x import Adafruit_NeoPixel, Color


# LED strip configuration:
LED_COUNT = 150      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Methods
NONE = 0
SET_COLOR = 1  # Requires color param
SET_N_COLORS = 2  # Requires array of colors
COLORS_LOOP = 3  # Requires array of colors, offset and interval


#  Color Helpers
def hex_to_rgb(hex: str) -> Tuple[int, int, int]:
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_color(rgb: Tuple[int, int, int]) -> Color:
    return Color(rgb[0], rgb[1], rgb[2])


class Strip(Adafruit_NeoPixel):

    def __init__(self) -> None:
        super().__init__(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                         LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

        self.action = None
        self.colors: List[Color] = []
        self.interval = None
        self.offset = None

    def clear(self):
        self.action = None
        self.colors = []
        self.interval = None
        self.offset = None

    def set_color(self, color: str):
        self.clear()
        self.colors = [hex_to_rgb(color)]
        self.action = self._set_color

    def _set_color(self):
        color = self.colors[0]
        for i in range(self.numPixels()):
            self.setPixelColor(i, rgb_to_color(color))
        self.show()

    def set_colors(self, colors: List[str]):
        self.clear()
        self.colors = [hex_to_rgb(color) for color in colors]
        self.action = self._set_colors

    def _get_fractional_color(self, fraction: float, previous: int) -> Color:
        next = previous + 1

        r = int(float(self.colors[next][0] - self.colors[previous]
                [0]) * fraction) + self.colors[previous][0]
        g = int(float(self.colors[next][1] - self.colors[previous]
                [1]) * fraction) + self.colors[previous][1]
        b = int(float(self.colors[next][2] - self.colors[previous]
                [2]) * fraction) + self.colors[previous][2]
        # print(r, g, b)
        return Color(r, g, b)

    def _get_pixels(self) -> List[Color]:
        pixels = []

        for i in range(LED_COUNT):
            # Find how far through the LEDS we are as a percentage
            position_ratio = float(i) / float(LED_COUNT)
            # Now we know how far through the colors we are
            previous_color = int(position_ratio * float(len(self.colors) - 1))

            if previous_color >= len(self.colors) - 1:
                pixels.append(rgb_to_color(self.colors[-1]))
                continue
            fraction = (position_ratio - (float(previous_color) /
                        float(len(self.colors) - 1))) * float(len(self.colors) - 1)
            # print(f"{i}, previous: {previous_color}, fractions: {fraction}")
            color = self._get_fractional_color(fraction, previous_color)

            pixels.append(color)

        return pixels

    def _set_colors(self):
        pixels = self._get_pixels()

        for i in range(self.numPixels()):
            color = pixels[i] if i < len(pixels) else Color(0, 0, 0)
            self.setPixelColor(i, color)
        self.show()
        self.clear()

    def set_color_loop(self, colors: List[str], delay: int):
        self.clear()
        self.interval = float(delay) / 1000.0
        self.offset = 0
        self.colors = [hex_to_rgb(color) for color in colors]
        self.action = self._set_color_loop

    def _set_color_loop(self):
        pixels = self._get_pixels()
        for i in range(self.numPixels()):
            index = i + self.offset
            if index >= LED_COUNT:
                index -= LED_COUNT
            color = pixels[index] if index < len(pixels) else Color(0, 0, 0)
            self.setPixelColor(i, color)

        self.offset = self.offset + 1 if self.offset < LED_COUNT else 0
        self.show()
        time.sleep(self.interval)

    def clear_strip(self, color: Color = None):
        for i in range(self.numPixels()):
            self.setPixelColor(i, Color(0, 0, 0) if color is None else color)
        self.show()

    def start(self):
        print("Starting")
        self.begin()
        print("Clearing")
        self.clear_strip(Color(10, 10, 10))
        try:
            while True:
                if self.action is not None:
                    self.action()
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            self.clear_strip()


if __name__ == "__main__":
    strip = Strip()
    strip.start()
