from cv2 import cv2

out_path = 'test' + '.mp4'

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot op                                                                            /en webcam")

ret, frame = cap.read()
height, width, layers = frame.shape
size = width, height
out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, size)

while True:
    ret, frame = cap.read()
    cv2.imshow('Input', frame)
    out.write(frame)

    c = cv2.waitKey(1)

    if c == ord(' '):
        break

out.release()
cap.release()
cv2.destroyAllWindows()
