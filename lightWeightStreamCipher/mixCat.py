def phepnhan(giatrimix, giatritext):
        # bit 7
        giatriphu = giatritext
        ketqua = 0x00       # xoa de luu gia tri
        if (giatrimix & 0x01) == 0x01:
                ketqua = ketqua ^ giatriphu
        # bit 6
        giatriphu = nhanvoi_x(giatriphu)
        if (giatrimix & 0x02) == 0x02:
                ketqua = ketqua ^ giatriphu
        # bit 5
        giatriphu = nhanvoi_x(giatriphu)
        if (giatrimix & 0x04) == 0x04:
                ketqua = ketqua ^ giatriphu
        # bit 4
        giatriphu = nhanvoi_x(giatriphu)
        if (giatrimix & 0x08) == 0x08:
                ketqua = ketqua ^ giatriphu
        # bit 3
        giatriphu = nhanvoi_x(giatriphu)
        if (giatrimix & 0x10) == 0x10:
                ketqua = ketqua ^ giatriphu
        # bit 2
        giatriphu = nhanvoi_x(giatriphu)
        if (giatrimix & 0x20) == 0x20:
                ketqua = ketqua ^ giatriphu
        # bit 1
        giatriphu = nhanvoi_x(giatriphu)
        if (giatrimix & 0x40) == 0x40:
                ketqua = ketqua ^ giatriphu
        # bit 0
        giatriphu = nhanvoi_x(giatriphu)
        if (giatrimix & 0x80) == 0x80:
                ketqua = ketqua ^ giatriphu
        return ketqua

def nhanvoi_x(giatri):
        if (giatri & 0x80) == 0x80:     # neu bit dau tien = 1
                ketqua = (giatri << 1) & 0xff    # dich trai gia tri di 1 don vi
                ketqua = ketqua ^ 0x1B  # xor voi 11011

        else:                           # bit dau tien = 0
                ketqua = giatri << 1
        return ketqua
