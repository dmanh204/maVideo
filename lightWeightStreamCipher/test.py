# import os
# try:
#     size = os.path.getsize('test.txt')
#     print(f'The size: {size}')
# except FileNotFoundError:
#     print("File not found.")
# except OSError:
#     print("OS error occured.")
import time
lis = []
with open('stream2.txt', 'r') as f:
    for i in range(20000):
        read = f.read(1)
        # if (read == ''):
            # break
        lis.append(int(read))
# print(lis)
# def Average(lis):
#     return sum(lis) /len(lis)
# a = Average(lis)
# print(f'The average number is: {a}')
s = time.time()
import LinearComplexity as lc
l = lc.runTest(lis)
e = time.time()
print(f"Linear complexity = {l}")
print('Time:', e-s)