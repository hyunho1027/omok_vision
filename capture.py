import cv2
import numpy as np
 
# Create a VideoCapture object
cap = cv2.VideoCapture(0)
 
# Check if camera opened successfully
if (cap.isOpened() == False): 
    print("Unable to read camera feed")

# pts1 = np.float32([[220,250],[170, 350],[400,255],[425,350]])

# pts2 = np.float32([[10,10],[10,290],[290,10],[290,290]])

# M = cv2.getPerspectiveTransform(pts1, pts2)
    
while(True):
    ret, frame = cap.read()
 
    if ret == True: 
         
        cv2.circle(frame, (223,255), 2, (255,0,0),-1)
        cv2.circle(frame, (171,348), 2, (255,0,0),-1)
        cv2.circle(frame, (403,260), 2, (255,0,0),-1)
        cv2.circle(frame, (425,360), 2, (255,0,0),-1)
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #gray_frame = cv2.warpPerspective(gray_frame, M, (300,300))
        
        
        # Display the resulting frame    
        cv2.imshow('frame',gray_frame)
        
        # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    # Break the loop
    else:
        break 

cap.release()
#out.release()
 
# Closes all the frames
cv2.destroyAllWindows() 