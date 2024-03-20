import cv2
import numpy as np
import sys
sys.path.insert(0, 'F:/TaiLieuHocTap/sip/StreamCipher/lightWeightStreamCipher')
import lightweight as lw
import math
video_path = "sample.mp4"
cap = cv2.VideoCapture(video_path)

frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

video_np_arr = np.array(frames)
print(video_np_arr.shape)
# Get number of frames, width, height, dimension.
n, w, h, d = video_np_arr.shape
# Calculate the size of total data that need to encrypt.
size = math.ceil(n*w*h*d/32)
# Generate key stream.
ma = lw.light(0xb5f576a31909777d) # Khoi tao
key = []
for _ in range(size):
    key.extend(ma.run())

# Encryption
key_np = np.array(key, dtype=np.uint8)

key_np = np.resize(key_np, video_np_arr.shape)

result = np.bitwise_xor(video_np_arr, key_np)

# Define the output video file path
output_video_path = "output_video.mp4"

# Get the height and width of the frames (assuming all frames have the same size)
frame_height, frame_width, _ = video_np_arr.shape[1:]

# Initialize the VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4 format
fps = 24  # Frames per second
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Write each frame to the output video
for frame in video_np_arr:
    out.write(frame)

# Release the VideoWriter and close the output file
out.release()

print(f"New video saved as {output_video_path}")
cap.release()
cv2.destroyAllWindows()
