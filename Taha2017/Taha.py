import math
import numpy as np
class Taha:
    def __init__(self,key, iv):
        self.P1 = 0xd92921a8
        self.P2 = 0b1101111011110000001111000010110
        self.Us = (iv&0xffffffff00000000) >> 32  # 0x3281395e
        self.Up = iv & 0xffffffff #0xbba3e74b
        self.Ks_1 =  (key&0xffffffff00000000) >>32
        self.Ks_2 = LS3bit(self.Ks_1)
        self.Ks_3 = LS3bit(self.Ks_2)
        self.Kp_1 =  key & 0xffffffff
        self.Kp_2 = LS3bit(self.Kp_1)
        self.Kp_3 = LS3bit(self.Kp_2)
        self.Q1 = self.Us
        self.Q2 = self.Up
        self.Xs_1 = self.Xs_2 = self.Xs_3 = self.Xp_1 = self.Xp_2 = self.Xp_3 = 1
    def SkewTentMap(self):
        Us = self.Us
        Ks_1 = self.Ks_1
        Ks_2 = self.Ks_2
        Ks_3 = self.Ks_3
        P1 = self.P1
        Q1 = self.Q1
        n = 32
        F1 = (Us + Ks_1 *self.Xs_1 +Ks_2 *self.Xs_2 +Ks_3*self.Xs_3)%(2**n)

        # skewTentMap
        if(0<self.Xs_1<P1):
            X0 = math.ceil(2**n *self.Xs_1/P1)%(2**n)
        elif(self.Xs_1 == P1):
            X0 = (2**n)-1
        elif(P1<self.Xs_1<2**n):
            X0 = math.ceil(2**n * (2**n - self.Xs_1)/(2**n - P1))%(2**n)
        # Tinh Xs:
        Xs = X0 ^ Q1
        # Update tham so:
        self.Xs_3, self.Xs_2, self.Xs_1 = self.Xs_2, self.Xs_1, Xs

    def PWLCMap(self):
        Up = self.Up
        Kp_1 = self.Kp_1
        Kp_2 = self.Kp_2
        Kp_3 = self.Kp_3
        P2 = self.P2
        Q2 = self.Q2
        n = 32

        F2 = (Up+ Kp_1 *self.Xp_1 + Kp_2 *self.Xp_2 + Kp_3 *self.Xp_3)%(2**n)
        # PWLC map:
        if(0<self.Xp_1<P2):
            X0 = math.ceil(2**n *self.Xp_1)%(2**n)
        elif(P2< self.Xp_1<2**(n-1)):
            X0 = math.ceil(2**n * (self.Xp_1 - P2)/(2**(n-1) - P2))%(2**n)
        elif(2^(n-1) < self.Xp_1 < 2**n - P2):
            X0 = math.ceil(2**n * (2**n - P2 - self.Xp_1)/(2**(n-1) - P2))%(2**n)
        elif(2**n - P2 < self.Xp_1 < 2**n - 1):
            X0 = math.ceil(2**n * (2**n - self.Xp_1)/P2)%(2**n)
        else:
            X0 = 2**n -1 -P2

        Xp = X0 ^ Q2
        # update tham so
        self.Xp_3, self.Xp_2, self.Xp_1 = self.Xp_2, self.Xp_1, Xp
    def run(self,iNumber):
        n = 32
        output = []
        for i in range(iNumber):
            self.SkewTentMap()
            self.PWLCMap()
            self.Q1 = LSFR(self.Q1)# update next value Q1
            self.Q2 = LSFR(self.Q2)# update next value Q2
            # Output Xg:
            if (0< (self.Xp_2 ^ self.Xs_2)<2**(n-1)):
                Xg = self.Xs_1
            else:
                Xg = self.Xp_1
            output.extend(split_32bit(Xg))
        return output
def LSFR(input):
        a = input
        for i in range(32):
            x = (a ^ (a>>10) ^ (a>>30) ^(a>>31))&0b1 # LFSR 32bit = x^32 + x^22 + x^2 +x^1
            a = ((x<<31)&0xffffffff)|(a>>1)
        return a    # Tra ve gia tri a la gia tri trong thanh ghi hien tai, gia tri output cua qua trinh LFSR thuc ra chinh la dau vao, ta dang tinh gia tri dau ra cua lan thuc hien ke tiep.
def LS3bit(a):
        a = ((a << 3)&0xffffffff) | (a >> 29)
        return a


# Bien cac so integer 32 bit thanh array cac so integer 8 bit.
def split_32bit(int32_val):
    # Convert the 32-bit integer to a binary string
    bin_str = np.binary_repr(int32_val, width=32)

    # Extract four 8-bit segments from the binary string
    int8_arr = [
        int(bin_str[0:8], 2),
        int(bin_str[8:16], 2),
        int(bin_str[16:24], 2),
        int(bin_str[24:32], 2)
    ]

    return int8_arr
# run the program
# iv = 0x3281395ebba3e74b
# key = 0x2641b709406e48c9
# test = Taha(key, iv)
#
# output = ""
# test.run(31250)
# with open("taha.manh.txt", "w") as f:
#     f.write(output)