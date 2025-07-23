import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.keys import Key
from kmk.scanners import DiodeOrientation

from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

from kmk.modules.layers import Layers

from kmk.extensions.RGB import RGB

from kmk.extensions.display import Display, TextEntry, ImageEntry


# inititalize keyboard isntance
keyboard = KMKKeyboard()

encoder_handler = EncoderHandler
keyboard.modules.append(encoder_handler)

keyboard.extensions.append(MediaKeys())

class RGBChange(RGB):
    def on_layer_change(self, layer):
        if layer == 0:
            self.set_hsv_fill(0, self.sat_default, self.val_default)   # red
        elif layer == 1:
            self.set_hsv_fill(170, self.sat_default, self.val_default) # blue
        elif layer == 2:
            self.set_hsv_fill(43, self.sat_default, self.val_default) # yelloe

        # update LEDs manually 
        self.show()

rgb = RGBChange(
    pixel_pin = board.GP9,
    num_pixels = 8,
    val_limit = 100,
    rgb_order = (1, 0, 2),
    hue_default = 0, 
    sat_default = 255,
    val_default = 100,
)

keyboard.extensions.append(rgb)

# old code
# class RGBLayers(Layers):
#     def activate_layer(self, keyboard, layer, idx=None):
#         super().activate_layer(keyboard, layer, idx)
#         rgb.on_layer_change(layer)

#     # def deactivate_layer(self, keyboard, layer):
#     #     super().deactivate_layer(keyboard, layer)
#     #     rgb.on_layer_change(keyboard.active_layers[0])

# keyboard.modules.append(RGBLayers())

# define which pins on XIAO the encoder uses
encoder_handler.pins = (
    (board.GP17, board.GP15, None,)
)

# defining the encoder functions (same across all layers)
# the button is not defined because it is wired into the key matrix
encoder_handler.map = [ 
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, ),), # layer 0
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, ),), # layer 1
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, ),), # layer 2
]

# defining what pins matrix columns and rows correspond to and putting them in the like cols and rows
COL0 = board.GP8
COL1 = board.GP4
COL2 = board.GP7
ROW0 = board.GP1
ROW1 = board.GP11
ROW2 = board.GP10

# putting them more in the columns and rows
keyboard.col_pins = (COL0, COL1, COL2)
keyboard.row_pins = (ROW0, ROW1, ROW2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
# tell it that the diodes are like pointing from columns 2 ("to") rows

# old code for custom key layer cycle
# LAYER_COUNT = 3
# def cycle_layer(keyboard, key):
#     current = keyboard.active_layers[0]
#     next = (current + 1) % LAYER_COUNT

#     keyboard.active_layers = [next]
#     rgb.on_layer_change(next)

#     return False

# new code that creates custom key derived from Key base class
class CycleKey(Key):

    # when defining, pass in the layer count DONT FORGET WHEN CHANGING YOU
    def __init__(self, layer_count):
        super().__init__()
        self.layer_count = layer_count

    # on press, find the next layer, if at end, cycle back to 0, set next as active, call rgb layer change
    def on_press(self, keyboard, coord_int=None):
        current = keyboard.active_layers[0]
        next_layer = (current + 1) % self.layer_count
        keyboard.active_layers = [next_layer]
        rgb.on_layer_change(next_layer) 

KC_CYCLE = CycleKey(3)

# encoder button wired in key matrix
# layer switch button puts the next layer on the top for a cycling effect (hopefully)

# assign actual keys later
keyboard.keymap = [
    # layer 0 - regular?
    [[KC.A,  KC.A,   KC_CYCLE],
    [KC.A,  KC.MEDIA_PLAY_PAUSE,   KC.A],
    [KC.A,  KC.A,   KC.A],],
    
    # layer 1 - gaming
    [[KC.A,  KC.A,   KC_CYCLE],
    [KC.A,  KC.MEDIA_PLAY_PAUSE,   KC.A],
    [KC.A,  KC.A,   KC.A],],

    # layer 2 - art
    [[KC.A,  KC.A,   KC_CYCLE],
    [KC.A,  KC.MEDIA_PLAY_PAUSE,   KC.A],
    [KC.A,  KC.A,   KC.A],],
]

from kmk.extensions.display.ssd1306 import SSD1306

bus = busio.I2C(board.GP6, board.GP5)

driver = SSD1306(
    i2c=bus,
    device_address=0x3C,
)

display = Display(
    display=driver,
    width=128,
    height=32,
    brightness = 0.8,
)

# make and change these to images later
display.entries = [
    TextEntry(text = "1", x = 0, y = 0, layer = 0),
    TextEntry(text = "2", x = 0, y = 0, layer = 1),
    TextEntry(text = "3", x = 0, y = 0, layer = 2),
]

keyboard.extensions.append(display)

if __name__ == '__main__':
    keyboard.go()