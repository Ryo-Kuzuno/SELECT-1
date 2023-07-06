import evdev

#検知したいデバイスのevent番号を書いてください
device = evdev.InputDevice('/dev/input/event0')

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        if event.value == 1: #0:UP, 1:DOWN
            if event.code == evdev.ecodes.KEY_KP1:
                print('KEY1')
            if event.code == evdev.ecodes.KEY_KP2:
                print('KEY2')
            if event.code == evdev.ecodes.KEY_KP3:
                print('KEY3')