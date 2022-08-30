## Counter IC used for rotary encoder
import struct
import spidev
from time import sleep
from functools import reduce

class LS7366R():

    CLEAR_MODE0   = 0x08
    CLEAR_MODE1   = 0x10
    CLEAR_COUNTER = 0x20
    CLEAR_STATUS  = 0x30
    READ_MODE0    = 0x48
    READ_MODE1    = 0x50
    READ_COUNTER  = 0x60
    READ_OTR      = 0x68
    READ_STATUS   = 0x70
    WRITE_MODE0   = 0x88
    WRITE_MODE1   = 0x90
    WRITE_DTR     = 0x98
    CLEAR_STATUS  = 0x30
    LOAD_COUNTER  = 0xE0
    LOAD_OTR      = 0xE4


    #   Count Operating Modes
    #   0x00: non-quadrature count mode. (A = clock, B = direction).
    #   0x01: x1 quadrature count mode (one count per quadrature cycle).
    #   0x02: x2 quadrature count mode (two counts per quadrature cycle).
    #   0x03: x4 quadrature count mode (four counts per quadrature cycle).
    FOURX_COUNT = 0x01

    #   Count Byte Modes
    FOURBYTE_COUNTER  = 0x00	# counts from 0 to 4,294,967,295
    THREEBYTE_COUNTER = 0x01	# counts from 0 to    16,777,215
    TWOBYTE_COUNTER   = 0x02	# counts from 0 to        65,535
    ONEBYTE_COUNTER   = 0x03	# counts from 0 to           255

    #   Enable/disable counter
    EN_CNTR  = 0x00  # counting enabled
    DIS_CNTR = 0x04  # counting disabled

    BYTE_MODE = [ONEBYTE_COUNTER, TWOBYTE_COUNTER, THREEBYTE_COUNTER, FOURBYTE_COUNTER]

    #----------------------------------------------
    # Constructor

    def __init__(self, cs_line, byte_mode):
        self.byte_mode = byte_mode

        self.spi = spidev.SpiDev()
        self.spi.open(0, cs_line) # Which CS line will be used
        self.spi.max_speed_hz = 100000 #Speed of clk (modifies speed transaction)

        #Init the Encoder
        self.clear_counter()
        self.clear_status()
        self.spi.xfer2([self.WRITE_MODE0, self.FOURX_COUNT])
        sleep(.1) #Rest
        self.spi.xfer2([self.WRITE_MODE1, self.BYTE_MODE[self.byte_mode-1]])

    def close(self):
        self.spi.close()

    def clear_counter(self):
        self.spi.xfer2([self.CLEAR_COUNTER])

    def clear_status(self):
        self.spi.xfer2([self.CLEAR_STATUS])

    def load_counter(self, enc_val):    # Counterに任意の値(enc_val)をセット。この値から計測開始。
        data = struct.pack(">I", enc_val)[-self.byte_mode:] # ビッグエンディアンのunsigned intに変換
        self.spi.xfer2([self.WRITE_DTR] + list(ord(k) for k in data))   # Unicodeに変換して転送
        self.spi.xfer2([self.LOAD_COUNTER]) #   OTRをCTRに転送

    def read_counter(self): # Counterの値を取得
        data = [self.READ_COUNTER] + [0] * self.byte_mode   # 2 Byte以降は転送において意味がない(ランダムな値)。それを良いことに変数を受信に利用するため5 Byte分確保。
        data = self.spi.xfer2(data)
        return reduce(lambda a,b: (a<<8) + b, data[1:], 0)  # 1byte*4 の配列unsigend intに変換

    def read_status(self):  # status(Counterの値のOverflowとか)の情報を取得
        data = self.spi.xfer2([self.READ_STATUS, 0xFF])
        return data[1]

    def set_count_mode(self, mode): # mode : 0~3. Count Operating Modesを参照
        self.spi.xfer2([self.WRITE_MODE0, (self.spi.xfer2([self.READ_MODE0])[1] & ~0b11) , self.FOURX_COUNT])

    def get_overflow(self): # Counterの値がcarryやborrowを起こしていないか監視する。こまめに実行して監視しても見逃すことが考えられるため、Counterの値の変動から推測するほうがよいかも。
        status = encoder.read_status()
        return 1 if status & (1<<7) else -1 if status & (1<<6) else 0

# if __name__ == "__main__":
    
#     encoder = LS7366R(0, 4) # Counterの値は4 Byte
#     encoder.read_counter()
#     # encoder.read_status()
