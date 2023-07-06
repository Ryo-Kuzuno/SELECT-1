import tty
import sys
import termios

def getkey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return key

while True:
    key = getkey()
    if key == 'q':
        print("input: q")
    # キー入力の処理
