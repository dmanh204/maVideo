import math
import struct
class Logistic3D:
    def __init__(self, xi, x1, yi, y1, zi, z1, a, b, c, lamda, rho, sigma):
        self.Xi = xi
        self.X1 = x1
        self.Yi = yi
        self.Y1 = y1
        self.Zi = zi
        self.Z1 = z1
        self.lamda = lamda
        self.rho = rho
        self.sigma = sigma
        self.a = a
        self.b = b
        self.c = c
    
    def run(self):
        #calculate 3D Logictic map
        x = mod(self.a * self.Xi * (1-self.Xi) + self.lamda * self.Y1)
        y = mod(self.b * self.Yi * (1-self.Yi) + self.rho * self.Z1)
        z = mod(self.c * self.Zi * (1-self.Zi) + self.sigma * self.X1)
        # update value
        self.X1 = self.Xi
        self.Xi = x
        self.Y1 = self.Yi
        self.Yi = y
        self.Z1 = self.Zi
        self.Zi = z
def mod(input):
    output = input - math.floor(input)
    return output

def Float2Bin(f):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]

# a = 0xffff0000 & Float2Bin(logistic.X1)
# a = a >> 16