import cv2
import mediapipe as mp
import pyautogui
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                #print(screen_x,"  ",screen_y)
                pyautogui.moveTo(screen_x, screen_y)

               
        down = [landmarks[145], landmarks[159]]
        for landmark in down:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
            dd=(down[0].y - down[1].y)
          #  print("difference",ld)
        if  dd< 0.01:
            pyautogui.press('left')
            #pyautogui.mouseDown()
            #pyautogui.sleep(2)
        up = [landmarks[0], landmarks[17]]

        for landmark in up:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
            ud=up[1].y-up[0].y
            #print(x,y," difference:   ",rd)
            if(ud>0.07):
                pyautogui.press('up')
                #pyautogui.mouseUp()
            #pyautogui.sleep(2)
                
        right = [landmarks[61], landmarks[287]]
        for landmark in right:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
            rd=right[0].y-right[1].y
           # print(x,y," difference of right:   ",rd)
            if(rd<0):
                pyautogui.press('down')
                #pyautogui.mouseUp()
             #   pyautogui.sleep(1)         
        #if (left[0].y - left[1].y) < 0.004:
         #   pyautogui.click()
          #  pyautogui.sleep(1)
            #pyautogui.sleep(2)
          
        left = [landmarks[257], landmarks[253]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
            ld=left[1].y-left[0].y
            print(x,y," difference:   ",ld)
            if(ld<0.033):
                pyautogui.press('right')
                #pyautogui.mouseUp()
    cv2.imshow('Eye Controlled Mouse', frame)
    key=cv2.waitKey(1)
    if key==27:
        break
