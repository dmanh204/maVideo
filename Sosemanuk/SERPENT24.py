Sbox = {0:[3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],
        1:[15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
        2:[8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],
        3:[0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
        4:[1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],
        5:[15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
        6:[7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],
        7:[1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]}
class SERPENT24:
    def __init__(self, key) -> None:
        self.initKey = key
        self.keySchedule()

    def int32to4(self,input): # Bien doi gia tri int 32 byte(256 bit) thanh list cac gia tri 4 byte
        ret = []
        for i in range(8):
            a = 0xffffffff << (i)*32
            a &= input
            a = a >> (i)*32

            ret.append(a)
        return ret
    
    def int16to4(self,input): # Bien doi gia tri int 16 byte(128 bit) thanh list cac gia tri 4 byte
        ret = []
        for i in range(4):
            a = 0xffffffff << (i)*32
            a &= input
            a = a >> (i)*32

            ret.append(a)
        return ret
    
    def ROTL(self, value, i): # Ham Rotate Left i bit cho word 32-bit
        a = pow(2, i) - 1
        a = a << (32 - i)
        a &= value
        a = a >> (32-i)
        value = (value << i) & 0xffffffff
        a = a | value
        return a
    
    def SboxExec(self, word, S_index):
        ret = 0
        for i in range(8):
            a = 0xf << (i*4) # 1111
            a &= word
            a = a >> (i*4)
            # Thuc hien subtitude
            a = Sbox[S_index][a]
            # Tra lai gia tri vao word
            a = a << (i*4)
            ret |= a
        return ret
    
    def Xor128(self, listA, listB):
        ret = []
        for i in range(4):
            ret.append(listA[i]^listB[i])
        return ret
            
    def keySchedule(self):
        listWord = self.int32to4(self.initKey) # Cho 8 word 32-bit (init key) vao list
        # Sinh ra 25 sub key, them word vao list:
        for i in range(8,108):
            a = listWord[i-8]^listWord[i-5]^listWord[i-3]^listWord[i-1]^0x9e3779b9^i
            a = self.ROTL(a, 11)
            listWord.append(a)
        # Cho cac word di qua Sbox
        listSubkey = []
        s_index = 3
        count = 0
        for i in listWord[8:108]:
            listSubkey.append(self.SboxExec(i,s_index))
            count = count+1
            if count == 4:
                count = 0
                s_index = (s_index-1)%8

        return listSubkey
    
    def LT(self, state):
        ret = [0,0,0,0]
        ret[0] = self.ROTL(state[0], 13)
        ret[2] = self.ROTL(state[2], 3)
        ret[1] = state[1] ^ ret[0] ^ ret[2]
        ret[3] = state[3] ^ ret[2] ^ self.ROTL(ret[0], 3)
        ret[1] = self.ROTL(ret[1],1)
        ret[3] = self.ROTL(ret[3],7)
        ret[0] = ret[0] ^ ret[1] ^ ret[3]
        ret[2] = ret[2] ^ ret[3] ^ self.ROTL(ret[1], 7)
        ret[0] = self.ROTL(ret[0], 5)
        ret[2] = self.ROTL(ret[2], 22)
        return ret

    def run(self, IV):
        ret = []
        listKey = self.keySchedule()
        listIV = self.int16to4(IV)
        for i in range(24): # 24 round
            roundKey = listKey[(i*4):(i*4+4)]
            listIV = self.Xor128(roundKey, listIV)
            for j in range(4):
                listIV[j] = self.SboxExec(listIV[j], i%8) # IV 128 bit, Sbox Exec 32 bit###
            for j in range(4):
                listIV = self.LT(listIV)
            if (i != 23):
                ret.append(listIV)
        roundKey = listKey[96:100]
        listIV = self.Xor128(roundKey, listIV)# Add round key #25 (round 24)
        ret.append(listIV)
        return ret

