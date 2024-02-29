mod = 256

class RC4:
    S = []
    i = j = 0

    def __init__(self, key) -> None:
        T = []
        for i in range(mod):
            self.S.append(i)
            T.append(key[i % len(key)])

        # Initial Permutation S
        j = 0
        for i in range(mod):
            j = (j + self.S[i] + T[i]) % mod
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def Generate(self):
        self.i = (self.i + 1) % mod
        self.j = (self.j + self.S[self.i]) % mod
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        t = (self.S[self.i] + self.S[self.j]) % mod
        return self.S[t]


# key = [100, 90, 176, 211, 45, 73, 192, 153, 235, 111, 74, 32]
# k = RC4(key)
# for i in range(10):
#     print(k.Generate())