import tty
import sys
import termios
import select

def getkey(timeout=0.1):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        r, _, _ = select.select([sys.stdin], [], [], timeout)
        if r:
            key = sys.stdin.read(1)
            return key
        else:
            return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

while True:
    key = getkey()
    if key == 'q':
        break
    elif key is not None:
        # キー入力があった場合の処理
        print("入力されたキー:", key)
    else:
        # タイムアウトした場合の処理
        print("入力待ち中...")
