import cv2 

video= cv2.VideoCapture(0)
faces=cv2.CascadeClassifier('/data/haarcascade_frontalface_default.xml')
while True:
    ret,frame = video.read()
    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Frame", frame)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()