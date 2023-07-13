import cv2
import time
import datetime
import winsound

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = True
AFTER_DETECTION=5

frame_size = (int(cap.get(3)),int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

#Started the while loop
while True :
    #Capture the fame 
    _, frame = cap.read()

#Convert our frame to gray scale 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#detects bodies and faces on the frame.
    faces = face_cascade.detectMultiScale(gray, 1.3 ,5)
    bodies = body_cascade.detectMultiScale(gray, 1.3 ,5)

 #Have you seen face and body
    if len(faces) + len(bodies) > 0:
     #Have detected before   
        if detection:
            timer_started = False
        else:
            detection = True
            #get the current time and date for each recording.
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc,20,frame_size)
            #Print start recording when record
            winsound.Beep(2500,1000)
            print("Started recording! ")
    
    elif detection:
        if timer_started:
            if ((time.time())- (detection_stopped_time >= AFTER_DETECTION)):
                detection = False
                timer_started= False
                out.release()
                print("Stop Recording")
        else:
            timer_started= True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    for (x,y , width ,height) in faces:
        cv2.rectangle(frame, (x,y,),(x + width, y + width), (255,0,0),3)
    
    #for (x,y , width ,height) in faces:
    #    cv2.rectangle(frame, (x,y,),(x + width, y + width), (255,0,0),3)


    cv2.imshow("Camera",frame)

    if cv2.waitKey(1)==ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()