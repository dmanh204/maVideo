import numpy as np
import sys
import math
import time
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/lightWeightStreamCipher')
import lightweight as lw
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/RC4')
import Rc4 as rc4
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/Salsa20')
import salsa20 as s20
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/Sosemanuk')
import SOSEMANUK as ssmn
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/Taha2017')
import Taha as th
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/Hybrid_stream')
import hybrid as hb
def xor_encrypt_decrypt(bin_np, key):
    key_np = np.array(key, dtype=np.uint8)
    key_np = np.resize(key_np, bin_np.shape) # Resize key stream  equal to binary stream.

    result = np.bitwise_xor(bin_np, key_np)
    return result

# File mp4 can ma hoa
mp4 = 'sample.mp4'
data = np.fromfile(mp4, dtype=np.dtype('B'))# Doc tu file binary .mp4 ra numpy array

# Khoi tao ma dong
sKey = []
print("1. RC4 \n2. Salsa20 \n3. Sosemanuk \n4. Taha \n5. Hybrid \n6. Proposed")
choice = int(input())
if choice == 1:
    key = [100, 90, 176, 211, 45, 73, 192, 153, 235, 111, 74, 32]
    k = rc4.RC4(key)
    st = time.perf_counter()
    for i in range(data.size):
        sKey.append(k.Generate())
    ed = time.perf_counter()
if choice == 2:
    key = "9e33bd7c6068e87fbe8aa2e7c5628f0d3699a5c5f108fdc1e995982028cbfb7c"
    nonce = "947cb4326dba6e79"
    ma = s20.Salsa20(key, nonce)
    st = time.perf_counter()
    for _ in range(math.ceil(data.size / 64)): # Vi mot lan chay salsa20 sinh ra 16 gia tri 4-byte = 64 byte
        sKey.extend(ma.run())
    ed = time.perf_counter()
if choice == 3:
    key = 0x2B32CA3BD845A26FF5005EDCB56D94BAF6CDE6936AC4CFB91A421DDC93DD6EB7
    initialVector = 0x72D242D18F56E1448BA1996C8344D669
    ma = ssmn.SOSEMANUK(key, initialVector)
    st = time.perf_counter()
    for _ in range(math.ceil(data.size / 16)): # Vi mot lan chay SOSEMANUK sinh ra 4 gia tri 4-byte
        sKey.extend(ma.run())
    ed = time.perf_counter()
if choice == 4:
    iv = 0x3281395ebba3e74b
    key = 0x2641b709406e48c9
    ma = th.Taha(key, iv)
    lanchay = math.ceil(data.size / 4) # Vi mot lan chay sinh ra 32 bit = 4 byte
    st = time.perf_counter()
    sKey = ma.run(lanchay)
    ed = time.perf_counter()
if choice == 5:
    ma = hb.hybrid()
    lanchay = math.ceil(data.size / 2)  # Vi mot lan chay sinh ra 16 bit = 2 byte
    st = time.perf_counter()
    sKey = ma.run(lanchay)
    ed = time.perf_counter()
if choice == 6:
    key = 0x1234567890abcdef
    ma = lw.light(key)
    st = time.perf_counter()
    for _ in range(math.ceil(data.size / 32)): # Vi mot lan chay light sinh ra 32 byte
        sKey.extend(ma.run())
    ed = time.perf_counter()
# Tien hanh ma hoa video bang ma dong
ketqua = xor_encrypt_decrypt(data, sKey)
output = ''.join(format(byte, '08b') for byte in ketqua)# chuyen cac phan tu trong numpy array tu dang binary
# sang dang string roi ghep vao output.
with open('TestHybrid.txt', 'w') as file: # Viet ket qua vao file .txt
    file.write(output)
ed2 = time.perf_counter()
print(f"Thoi gian sinh khoa: {ed - st:0.2f}s")
print(f"Thoi gian thuc thi: {ed2 - st:0.2f}s")