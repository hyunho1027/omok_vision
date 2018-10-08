import cv2
import numpy as np
import time
import json
import urllib.request

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False): 
    print("Unable to read camera feed")

turn_url = "http://pub.inspace.co.kr:10200/turn_status"
action_url = "http://pub.inspace.co.kr:10200/action?action_idx="
end_url =  "http://pub.inspace.co.kr:10200/periodic_status"
# first_url = "http://pub.inspace.co.kr:10200/enemy_action_index_status"

pts1 = np.float32([[223,255],[171, 348],[403,260],[425,360]])

pts2 = np.float32([[0,0],[0,300],[300,0],[300,300]])

M = cv2.getPerspectiveTransform(pts1, pts2)

x = [22,54,84,115,146,176,206,236,266]
y = [22, 52, 84, 115, 146, 177, 205, 235, 265]

is_End = False

while(1):

    
    end_response = urllib.request.urlopen(end_url)
    end_result = json.loads(end_response.read().decode('utf-8'))
    
    if end_result['win_index'] == 0 : #End Check
        is_End = False
        print("Not End!")
    else:
        print("End!")

    while not is_End:
        
        turn_response = urllib.request.urlopen(turn_url)
        turn_result = json.loads(turn_response.read().decode('utf-8'))

        time.sleep(1)
        if turn_result['curr_turn'] == turn_result['enemy_turn'] : #Turn Check
            # Not player turn
            print("Omok Turn!")
            

        else:
            print("Player Turn!")
            # Player turn
            is_Change = False

            # time delay or stable check
            time.sleep(5)
            ret, frame = cap.read()
            pre_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            pre_frame = cv2.warpPerspective(pre_frame, M, (300,300))
            pre_frame = pre_frame[10:290,10:290]
            cv2.imshow('pre_frame', pre_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            while not is_Change:
                frame_list = []

                is_Stable = False

                while not is_Stable:

                    ret, frame = cap.read()
                    cur_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    grid_frame = cv2.warpPerspective(cur_frame, M, (300,300))
                    grid_frame = grid_frame[10:290,10:290]
                    cur_frame = cv2.warpPerspective(cur_frame, M, (300,300))
                    cur_frame = cur_frame[10:290,10:290]
                    for i in x:
                        for j in y:
                            cv2.circle(grid_frame, (i,j), 2, (255), -1)
                    
                    cv2.imshow('grid_frame', grid_frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    
                    if ret == True :
                        cv2.imshow('cur_frame', cur_frame)
                        time.sleep(1)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        if len(frame_list):
                            frame_list = np.append(frame_list,np.array([cur_frame]),axis=0)
                            cv2.imshow('cur_frame',cur_frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                        else:
                            frame_list = np.array([cur_frame])

                        if len(frame_list) == 5 :
                            
                            # Stable Check
                            if np.max(np.std(frame_list,axis=0)) < 20:
                                is_Stable = True
                                print('Stable!')

                            else:
                                print(np.max(np.std(frame_list,axis=0)))
                                frame_list = frame_list[1:]
                                print('Not Stable!')
                    else:
                        break
                # Change Check

                if np.max(cv2.absdiff(pre_frame,cur_frame)) > 100:
                    is_Change = True
                    check_frame = cv2.absdiff(pre_frame,frame_list[-1])
                    x_check_frame = np.argmax(np.sum(check_frame, axis=0))
                    y_check_frame = np.argmax(np.sum(check_frame, axis=1))
                    cv2.circle(check_frame, (x_check_frame,y_check_frame), 2, (255), -1)

                    cv2.imshow('check_frame', check_frame)
                    time.sleep(1)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    x_idx, y_idx = 0,0
                    for i, _x in enumerate(x):
                        if _x+3 >= x_check_frame:
                            x_idx = i
                            break
                    for j, _y in enumerate(y):
                        if _y >= y_check_frame:
                            y_idx = j
                            break
                        
                    
                    output_idx = x_idx + 9*y_idx
                    print(x_idx, y_idx, output_idx)
                    #action_response = urllib.request.urlopen(action_url + str(output_idx))
                    #action_result = json.loads(action_response.read().decode('utf-8'))
                    

                    print('Change!')
                else:
                    print('Not Change!')
                    
        end_response = urllib.request.urlopen(end_url)
        end_result = json.loads(end_response.read().decode('utf-8'))            
        if end_result['win_index'] != 0 :
            is_End = False
