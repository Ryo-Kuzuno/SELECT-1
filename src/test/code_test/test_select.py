import sys
import select

def main():
    while True:
        # 標準入力の状態を監視
        r, _, _ = select.select([sys.stdin], [], [], 0.1)
        if r:
            # キー入力の処理
            key = sys.stdin.read(1)
            if key == 'q':
                break

if __name__ == '__main__':
    main()
