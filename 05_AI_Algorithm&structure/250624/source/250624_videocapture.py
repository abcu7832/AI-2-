#26p 동영상 파일을 읽고 보여주기
#import numpy as np
#import cv2

#cap = cv2.VideoCapture("son.mp4")
#while(cap.isOpened()):
#while True:
#    ret, frame = resized.read()

    #if ret is False:
    #    print("Can't receive frame (stream end?). Exiting ...")
    #    cap = cv2.VideoCapture("son.mp4") #######추가#######
    #    break

    #cv2.imshow("Frame", frame)

    #if cv2.waitKey(55) & 0xFF == ord('q'):
    #    cap.release()
    #    cv2.destroyAllWindows()
    #    exit()      

#if cv2.waitKey(5) & 0xFF == ord('q'):
#    break
# 전체 주석 처리 하는 방법: 명령모드에서 5,10s/^/#/ => 5~10줄 주석처리 
# 주석 해제: 5,10s/^#// => 5~10줄 주석해제

import numpy as np
import cv2
import os

cap = cv2.VideoCapture("son.mp4")

save_count = 0

save_dir = 'captures'
os.makedirs(save_dir, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    height, width = frame.shape[:2]
    resized = cv2.resize(frame, (width//2, height//2))

    cv2.imshow("Resized Frame", resized)

    #cv2.imshow("Frame", frame)

    key = cv2.waitKey(33)
    if key & 0xFF == ord('q'):
        break
    
    # 'c'키 누를 때 저장 overwrite 방지
    if key & 0xFF == ord('c'):
        #파일명 중복 피하기
        while True:
            filename = os.path.join(save_dir, f"capture_{save_count}.jpg")
            if not os.path.exists(filename):
                break
            save_count += 1
        cv2.imwrite(filename, frame)
        print(f"Saved:{filename}")
        save_count += 1