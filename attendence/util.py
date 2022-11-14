import cv2
import os
import time
import threading

t = 0
def timer():
    global t
    while t < 20:
        print("WORKING>>>")
        time.sleep(5)
        t+=5

def video_to_frames(path):
    # extract frames from a video and save to directory as 'x.png' where 
    # x is the frame index
    vidcap = cv2.VideoCapture(0)
    # cv2.namedWindow("Window")
    flag = False
    def window():
        count = 0
        global t
        while vidcap.isOpened():
            print(t)
            success, image = vidcap.read()
            cv2.imshow("Window", image)
            if success:
                print('yes')
                cv2.imwrite(os.path.join(path,'%d.png')% count, image)
                count += 1
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if t == 20:
                break
        t = 0
        cv2.flip(image,1)
    t1 = threading.Thread(target=timer)
    t2 = threading.Thread(target=window)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    cv2.destroyAllWindows()
    vidcap.release()