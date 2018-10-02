import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False): 
    print("Unable to read camera feed")

is_End = False

# pts1 = np.float32([[90,65],[0,230],[570,75],[640,240]])

# pts2 = np.float32([[10,10],[10,290],[290,10],[290,290]])

# M = cv2.getPerspectiveTransform(pts1, pts2)

pre_frame = cv2.imread('pre_frame.png')
pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_BGR2GRAY)     
while(not is_End):
    is_Change = False
    
    while(not is_Change):
            frame_list = []
            
            is_Stable = False
            while(not is_Stable):
                ret, frame = cap.read()
                cv2.circle(frame, (90,65), 2, (255,0,0),-1)
                cv2.circle(frame, (0,230), 2, (255,0,0),-1)
                cv2.circle(frame, (570,75), 2, (255,0,0),-1)
                cv2.circle(frame, (640,240), 2, (255,0,0),-1)

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # gray_frame = cv2.warpPerspective(gray_frame, M, (300,300))

                if ret == True:
                    cv2.imshow('omok',gray_frame)
                    # time.sleep(1)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    if len(frame_list):
                        frame_list = np.append(frame_list,np.array([gray_frame]),axis=0)
                    else:
                        frame_list = np.array([gray_frame])
                    
                    if len(frame_list) == 5 :
                        if np.max(np.std(frame_list,axis=0)) < 50:
                            is_Stable = True
                            # cv2.imwrite('pre_frame.png',frame_list[-1])
                            print('Stable!')
                        else:
                            print(np.max(np.std(frame_list,axis=0)))
                            frame_list = frame_list[1:]
                            print('Not Stable!')

                else:
                    break
            
            if np.mean(abs(pre_frame - frame_list[-1])) > 10:
                print(np.mean(abs(pre_frame - frame_list[-1])))
                is_Change = True
                check_frame = abs(pre_frame - frame_list[-1])
                cv2.imshow('check_frame',check_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                time.sleep(5)
                print('Change!')
            else:
                print('Not Change!')

    cv2.imwrite('pre_frame.png',frame_list[-1])
    is_End = True
    print('End!')
    
cap.release()
cv2.destroyAllWindows() 