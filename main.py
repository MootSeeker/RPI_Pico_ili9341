# Demo of drawing a screen on display with touch
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI

class Screen(object): 
    # Simple screen demo
    CYAN    = color565(0, 255, 255)
    RED     = color565(255, 0, 0)
    PURPLE  = color565(255, 0, 255)
    WHITE   = color565(255, 255, 255)

    def __init__(self, spi1, spi2):
        """ Übergabe: 
          - display (ili9431): Display object
          - touch (XPT2046): Touch object
        """
        self.display = Display(spi1, 
                               dc=Pin(15), 
                               cs=Pin(17), 
                               rst=Pin(14))     # Pin definition for D/C, CS and Reset signals
    
        self.touch = Touch(spi2, 
                           cs=Pin(13), 
                           int_pin=Pin(9),
                           int_handler=self.touchscreen_press)

        """ Start Screen nach init """
        self.display.draw_text8x8(100, 
                                  20, 
                                  "Welcome", 
                                  self.WHITE, 
                                  0)
        
        self.display.rotation = 0
        self.show_screen()
        
         # A small 5x5 sprite for the dot
        self.dot = bytearray(b'\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00')

    def touchscreen_press(self, x, y): 
        """Process touchscreen press events."""
        # Display coordinates
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "{0:03d}, {1:03d}".format(x, y),
                                  self.CYAN)
        
        # draw a dot where pressed
        self.display.draw_sprite(self.dot, x, y, 5, 5)

        # if welcome button pressed
        if 50 <= x <= 200 and 10 <= y <= 35:
            self.display.draw_text8x8(100, 100, "Hi :)", self.WHITE, 0, 0)

        # if Clear button pressed
        if 0 <= x <= 75 and 150 <= y <= 175: 
            self.display.clear()
            self.show_screen()

    def show_screen(self): 
        self.display.draw_rectangle(50, 10, 150, 25, self.CYAN)
        self.display.draw_text8x8(100, 20, "Welcome", self.WHITE, 0)
        self.display.draw_rectangle(0, 150, 75, 25, self.RED)
        self.display.draw_text8x8(20, 160, "Clear", self.WHITE)

def main():
    """ Test Code """
    # Init SPI0 for display
    spi1 = SPI( 0,                    # Used Hardware SPI
                baudrate=40000000,    # SPI Clock speed (Baudrate in Hz)
                polarity=1,           # Signal Polarity (Standby signal state)
                phase=1,              # Sample edge
                bits=8,               # Bits per data value
                firstbit=SPI.MSB,     # Byte order
                sck=Pin(18),          # Clock pin definition
                mosi=Pin(19),         # Data out pin definition
                miso=Pin(16))         # Data in pin definition
    
    # Init SPI1 for touchscreen
    spi2 = SPI(1,
               baudrate=5000000,
               sck=Pin(10), 
               mosi=Pin(11), 
               miso=Pin(12))
    
    Screen(spi1, spi2)

    # Draw a rectangle

    try: 
        while True: 
            idle()
    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")

# Run main application
main()

