from SOSEMANUK import SOSEMANUK
key = 0x2B32CA3BD845A26FF5005EDCB56D94BAF6CDE6936AC4CFB91A421DDC93DD6EB7
initialVector = 0x72D242D18F56E1448BA1996C8344D669
output = ""

Sose = SOSEMANUK(key, initialVector)
for i in range(7900):
    output += Sose.run()

with open("sosemanuk.manh.txt", "w") as f:
    f.write(output)