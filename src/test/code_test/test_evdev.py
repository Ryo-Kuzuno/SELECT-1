import evdev

#検知したいデバイスのevent番号を書いてください
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
    print(device.path, device.name, device.phys)

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