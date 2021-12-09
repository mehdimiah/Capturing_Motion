import cv2,time,pandas
from datetime import datetime
import numpy as np

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
#avi file of motion

first_frame = None
#need to capture a static background to form a foundation image for opencv

status_list = [None,None]
#none added as python is searching for the second to last item but it doesnt exist so none allows it to 'exist'
times = []

df = pandas.DataFrame(columns = ["Start","End"])
#creating a dataframe with no values but two columns start and end


video = cv2.VideoCapture(0)
#0,1,2 to index for a camera connected to the computer, a video file can be refferred to via ""

while True:
   
    check,frame = video.read()
    #check is a bool true if cam is working
    #frame is the actual frames fed by the camera itself
    status = 0 #no motion in frame


    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #converting frames into grey and storing them into the grey variable
    grey = cv2.GaussianBlur(grey, (21,21), 0)
    #removing noise from the images using GaussianBlur

    if first_frame is None:
        first_frame  = grey
        continue
    #setting the first frame as the first frame
    delta_frame = cv2.absdiff(first_frame, grey)
    #difference between the two frames

    thresh_frame = cv2.threshold(delta_frame, 30,255, cv2.THRESH_BINARY)[1] #thresh binary returns a tuple, [1] access the second value which is the frame itself
#classiying vals, if the diff between first frame and grey is 30, we will classify as 255 white (something in frame)
#if the diff is less than 30, assign it black pixel as in no movement

    thresh_frame = cv2.dilate(thresh_frame, None,iterations = 5)
    #removing black spots and making it cleaner and less noisy
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #all contours of objectis in the image and stored in cnts variable this measures the area within the contours (white blobs) to decipher movement
    for contour in cnts:
        if cv2.contourArea(contour) < 1000: #if area of contour is less than 1000 pixels go to next contour
            continue
        
        status = 1

        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 3)
        #drawing the rectangle 
        cv2.putText(frame, "Motion Detected", (0, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (0,35), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        #out.write(frame)
        #recording when motion is detected
    
        
    status_list.append(status)
    #this list shows if object is in frame or not 1 yes 0 no
    
    status_list = status_list[-2:]
    #cuttting for memory saving, the list to the last two digits instead of creating a massive llist
    
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
        #meauring when motion is captured as the last number in list will be 1 
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())      
        #measuring when the status turns to 0 and motion leaves the frame 

    #cv2.imshow("capturing",grey)
    #cv2.imshow("delta frame",delta_frame) #greyscale version blurried, 
    #cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("frame",frame)


   
    key = cv2.waitKey(1)
    if key == ord("q"):
        if status == 1:
            times.append(datetime.now())
            #when q is pressed to quit window when motion still in frame, this will add a end time to the times list
        break

#print(status_list)
#printning when motion detected in list
#print(times) #printing what times motion detected

for i in range(0,len(times),2): #iterating through the list with a step of two, iterating the amount of times as contents
    df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
    
df.to_csv("Times.csv")

    


#out.release()
#release the motion video
video.release()
cv2.destroyAllWindows()