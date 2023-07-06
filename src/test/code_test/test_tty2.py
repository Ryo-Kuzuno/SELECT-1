import tty
import sys
import termios

def getkey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        key = sys.stdin.read(3)  # エスケープシーケンス全体を読み取る
        if key == '\x1b[A':
            return 'Up'
        elif key == '\x1b[B':
            return 'Down'
        elif key == '\x1b[C':
            return 'Right'
        elif key == '\x1b[D':
            return 'Left'
        else:
            return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

while True:
    key = getkey()
    if key == 'q':
        break
    elif key == 'Up':
        # 上矢印キーの処理
    elif key == 'Down':
        # 下矢印キーの処理
    elif key == 'Right':
        # 右矢印キーの処理
    elif key == 'Left':
        # 左矢印キーの処理
    else:
        # その他のキー入力の処理