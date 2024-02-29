import math
pi2 = 2*math.pi
class Standard:
    def __init__(self, x, y, k) -> None:
        # x, y in [0,N], N = 16
        self.x = x
        self.y = y
        self.k = k

    def cal(self, rx, ry):
        self.x = (self.x + self.y + rx)%16 # x(i+1) = mod(x(i)+y(i) + rx)
        self.y = (self.y + self.k * math.ceil(math.sin(self.x * 16/pi2)) + ry) % 16 # y(i+1) = y(i) + 
        # Ksin(x(i+1)*16/2pi) + ry , self.x da update
