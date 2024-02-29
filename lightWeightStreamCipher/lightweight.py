from Standard import Standard
from mixCat import phepnhan
import time
# Sbox for substitution stage, from AES doc
sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
class light:
    def __init__(self, seed) -> None:
        # Init IS
        self.vector = []
        self.vector.append((0xff00000000000000 & seed) >> 56)
        self.vector.append((0xff000000000000 & seed) >> 48)
        self.vector.append((0xff0000000000 & seed) >> 40)
        self.vector.append((0xff00000000 & seed) >> 32)
        self.vector.append((0xff000000 & seed) >> 24)
        self.vector.append((0xff0000 & seed) >> 16)
        self.vector.append((0xff00 & seed) >> 8)
        self.vector.append(0xff & seed)
        for i in range(24):
            self.vector.append(0x00)
        # Init Standard map
        self.stan = Standard(1, 1, 1)
        
        # Init cat map
        self.cat = [1, 1, 1, 1,
                    1, 2, 1, 1,
                    1, 1, 1, 1,
                    1, 1, 1, 1]
    # Ham Sbox thuc hien sub Byte thong qua sbox.
    def Sbox(self, inp):
        hang = (0xf0 & inp) >> 4    # 4 byte dau la hang
        cot = 0x0f & inp            # 4 byte sau la cot
        ret = sbox[hang*16 + cot]
        return ret
    def subByte(self, vector):
        ret = []
        for i in range(32):
            ret.append(self.Sbox(vector[i]))
        return ret
    # Ham standard su dung standard map de permute bit
    # Thu hien permute bit n = 10 lan
    def Stand(self, vector, rx, ry): # thuc hien voi list 32 phan tu
        for i in range(10):
            hang1 = self.stan.x # x la hang
            cot1 = self.stan.y  # y la cot
            so1 = self.findBit(hang1, cot1)

            # Thuc hien 1 lan tinh standard map
            self.stan.cal(rx, ry)
            
            # Lay gia tri bit moi
            hang2 = self.stan.x
            cot2 = self.stan.y
            so2 = self.findBit(hang2, cot2)

            vector[so1], vector[so2] = self.swapBit(vector[so1], cot1, vector[so2], cot2)
        return vector # Tra lai vector moi da doi bit

    def findBit(self, hang, cot):
        # xac dinh byte nao co bit can tim
        chiSo = hang*2
        if cot >= 8:
            chiSo = chiSo + 1
        return chiSo
    def swapBit(self, a, cot1, b, cot2):
        xa = cot1 %8
        a1 = 0x01 << (7 - xa)
        a1 = a1 & a # Lay duoc bit xa
        a2 = 0xff&(-a1 -1) # nghich dao cua a1
        a = a2 & a # Xoa bit xa cua a

        xb = cot2 %8
        b1 = 0x01 << (7 - xb)
        b1 = b1 & b # Lay duoc bit xb
        b2 = 0xff & (-b1 - 1) # Nghich dao cua b1
        b = b2 & b # Xoa bit xb cua a

        if xa < xb:
            a1 = a1 >> (xb-xa)
            b1 = b1 << (xb-xa)
        elif xa > xb:
            a1 = a1 << (xa-xb)
            b1 = b1 >> (xa-xb)

        # thuc hien dua bit a vao b va dua bit b vao a
        a = a | b1
        b = b | a1
        return a, b
    
    # Thu hien Mix Byte
    def mixByte(self, vector, a, b):
        # update the Cat matrix
        self.cat[0] = (2* a *b + 2) %256
        self.cat[1] = (2* b) %256
        self.cat[2] = (a* b + 1) %256
        self.cat[3] = b %256
        self.cat[4] = 2* a %256
        self.cat[6] = a% 256
        self.cat[8] = (a* b+ 1) %256
        self.cat[9] = b %256
        self.cat[10] = (a* b +1) %256
        self.cat[11] = b %256
        self.cat[12] = a %256
        self.cat[14] = a % 256
        
        # Thuc hien mix byte
        ret = []
        for j in range(8):
            for i in range(4):
                m = phepnhan(self.cat[i*4], vector[j*4])
                n = phepnhan(self.cat[i*4 + 1], vector[j*4 + 1])
                p = phepnhan(self.cat[i*4 + 2], vector[j*4 + 2])
                q = phepnhan(self.cat[i*4 + 3], vector[i*4 + 3])
                ret.append(m ^ n ^ q ^ p)
        return ret
    
    # Let's do it
    def run(self):
        # Sbox
        v1 = self.subByte(self.vector)
        # Lay ra rx, ry, ki cho standard
        self.stan.k = v1[0]

        v2 = self.Stand(v1, v1[1], v1[2]) # rx = v1[1], ry = v1[2]

        # a = v2[30], b= v2[31]
        v3 = self.mixByte(v2, v2[30], v2[31])
        # update self.vector cho lan lap sau
        arr = []
        for i in range(32):
            self.vector[i] = v3[i]
            arr.append(v3[i])
        return arr
