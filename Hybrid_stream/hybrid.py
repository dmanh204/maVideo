from Chen_system import Chen
from Logistic import Logistic3D
from Logistic import Float2Bin
import numpy as np
class hybrid:
    def __init__(self):
        # Initial - tao gia tri khoi dau a.k.a IV and key
        self.chen = Chen(0.1, 0.1, 0.1, 35, 3, 28)
        # d = 35, e = 3, f, 28
        # u(0) = v(0) = w(0) = 0.1
        self.logistic = Logistic3D(0.1, 0.2, 0.3, 0.2, 0.2, 0.2, 1, 2.5, 4, 1, 2, 3)
        # x(1) = 0.1, y(1) = 0.2, z(1) = 0.3, x(2) = 0.2 , y(2) = 0.2, z(2) = 0.2
        # a = 1, b = 2.5, c = 4, lamda = 1, rho = 2 sigma = 3
    def eightBits(self, u, v, w):
        s = 10000*(u+v+w+50)
        s = Float2Bin(s) # Lay ra 8 bit least significant
        s = 0xff & s
        return s
    def updateLogis(self):
        # chay chen system va thuc hien mix state
        self.chen.run()
        s1 = self.eightBits(self.chen.u, self.chen.v ,self.chen.w) # s1 = 10000* (u1+v1+w1)%256
        self.chen.run()
        s2 = self.eightBits(self.chen.u, self.chen.v ,self.chen.w) # s2 = 10000* (u2+v2+w2)%256
        # Parameter varrying
        b = self.merge8to16(s1, s2)
        self.logistic.a = b


    def merge8to16(self, b1, b2):
        a_ = (b1<<8)|b2 # [b1,b2] 16bit
        a_ = a_ * self.logistic.a /(2**16) # a' = a*[b1,b2] /2^16
        return a_
    def byte2bin(self, int): # Bien doi 16 bit word (int) thanh string 16 binary
        string = ""
        for i in range(16):
            x = 0b00000001 << (15 - i)
            x = x & int
            x = x >> (15 - i)
            string += str(x)
        return string
    def run(self, iN):
        ret = []
        self.updateLogis()
        for i in range(iN):
            self.logistic.run()
            x = self.logistic.Xi
            x = Float2Bin(x) & 0xffff
            y = self.logistic.Yi
            y = 0xffff & Float2Bin(y)
            z = self.logistic.Zi
            z = 0xffff & Float2Bin(z)

            # generate key
            k = x ^ y ^ z
            # write key
            ret.extend(split_16bit(k))
            # control 
            if (iN %10 == 0):
                self.updateLogis()
        return ret

# Bien cac so integer 16 bit thanh array cac so integer 8 bit.
def split_16bit(int16_val):
    # Convert the 32-bit integer to a binary string
    bin_str = np.binary_repr(int16_val, width=16)

    # Extract four 8-bit segments from the binary string
    int8_arr = [
        int(bin_str[0:8], 2),
        int(bin_str[8:16], 2)
    ]

    return int8_arr
# a = hybrid()
# x = a.run(62500)
#
# with open ("hybrid.manh.txt", 'w') as f:
#     f.write(x)