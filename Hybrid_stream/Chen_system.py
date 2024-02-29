class Chen:
    def __init__(self, u, v, w, d, e, f):
        self.u = u # u(0)
        self.v = v # v(0)
        self.w = w # w(0)
        # d,e,f in the chaotic range
        self.d = d
        self.e = e
        self.f = f
    def run(self):
        h = 0.001
        # Su dung Runge-Kutta bac 4 de mo phong Chen system
        # Tinh gia tri K_1
        k11 = self.d * (self.v - self.u)
        k21 = (self.f - self.d) * self.u + self.f * self.v - self.u *self.w
        k31 = self.v * self.u -self.e *self.w
        # Tinh gia tri K_2
        k12 = self.d * ((self.v + h/2 * k21) - (self.u + h/2 * k11))
        k22 = (self.f -self.d) * (self.u + h/2 *k11) + self.f *(self.v + h/2 * k21) - (self.u + h/2 *k11) * (self.w +h/2 *k31)
        k32 = (self.v + h/2 * k21) * (self.u + h/2 * k11) - self.e * (self.w + h/2 * k31)
        # Tinh gia tri K_3
        k13 = self.d * ((self.v + h/2 * k22) - (self.u + h/2 * k12))
        k23 = (self.f -self.d) * (self.u + h/2 *k12) + self.f *(self.v + h/2 * k22) - (self.u + h/2 *k12) * (self.w +h/2 *k32)
        k33 = (self.v + h/2 * k22) * (self.u + h/2 * k12) - self.e * (self.w + h/2 * k32)
        # Tinh gia tri K_4
        k14 = self.d * ((self.v + h * k23) - (self.u + h * k13))
        k24 = (self.f -self.d) * (self.u + h *k13) + self.f *(self.v + h * k23) - (self.u + h *k13) * (self.w + h *k33)
        k34 = (self.v + h * k23) * (self.u + h * k13) - self.e * (self.w + h * k33)
        # Tinh gia tri u,v, w moi
        self.u = self.u + h/6 * (k11 + 2*k12 + 2*k13 + k14)
        self.v = self.v + h/6 * (k21 + 2*k22 + 2*k23 + k24)
        self.w = self.w + h/6 * (k31 + 2*k32 + 2*k33 + k34)