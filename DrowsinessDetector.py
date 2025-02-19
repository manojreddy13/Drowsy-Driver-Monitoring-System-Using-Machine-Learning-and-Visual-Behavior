from tkinter import *
import tkinter
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from playsound import playsound


main = tkinter.Tk()
main.title("Driver Drowsiness Monitoring")
main.geometry("500x400")

def EAR(drivereye):
    point1 = dist.euclidean(drivereye[1], drivereye[5])
    point2 = dist.euclidean(drivereye[2], drivereye[4])
    # compute the euclidean distance between the horizontal
    distance = dist.euclidean(drivereye[0], drivereye[3])
    # compute the eye aspect ratio
    ear_aspect_ratio = (point1 + point2) / (2.0 * distance)
    return ear_aspect_ratio
def MOR(drivermouth):
    # compute the euclidean distances between the horizontal
    point   = dist.euclidean(drivermouth[0], drivermouth[6])
    # compute the euclidean distances between the vertical
    point1  = dist.euclidean(drivermouth[2], drivermouth[10])
    point2  = dist.euclidean(drivermouth[4], drivermouth[8])
    # taking average
    Ypoint   = (point1+point2)/2.0
    # compute mouth aspect ratio
    mouth_aspect_ratio = Ypoint/point
    return mouth_aspect_ratio
    
def startMonitoring():
    pathlabel.config(text="          Webcam Connected Successfully")
    webcamera = cv2.VideoCapture(0)
    svm_predictor_path = 'SVMclassifier.dat'
    EYE_AR_THRESH = 0.25
    EYE_AR_CONSEC_FRAMES = 10
    MOU_AR_THRESH = 0.8
   

    COUNTER = 0
    yawnStatus = False
    yawns = 0
    #def play_alarm():
    	#playsound('war.wav')
    svm_detector = dlib.get_frontal_face_detector()
    svm_predictor = dlib.shape_predictor(svm_predictor_path)
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    while True:
        ret, frame = webcamera.read()
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_yawn_status = yawnStatus
        rects = svm_detector(gray, 0)
        for rect in rects:
            shape = svm_predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            mouth = shape[mStart:mEnd]
            leftEAR = EAR(leftEye)
            rightEAR = EAR(rightEye)
            mouEAR = MOR(mouth)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            mouthHull = cv2.convexHull(mouth)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 255), 1)
            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
            # Create a function to play an alarm sound
            #def play_alarm():
                  #playsound('alarm.wav')
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                cv2.putText(frame, "Eyes Closed ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
            else:
                COUNTER = 0
                cv2.putText(frame, "Eyes Open ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (480, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if mouEAR > MOU_AR_THRESH:
                cv2.putText(frame, "Yawning, DROWSINESS ALERT! ", (10, 70),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                yawnStatus = True
                output_text = "Yawn Count: " + str(yawns + 1)
                cv2.putText(frame, output_text, (10,100),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0),2)
            else:
                yawnStatus = False
            if prev_yawn_status == True and yawnStatus == False:
                yawns+=1
            cv2.putText(frame, "MAR: {:.2f}".format(mouEAR), (480, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame,"Visual Behaviour & Machine Learning Drowsiness Detection @ Drowsiness",(370,470),cv2.FONT_HERSHEY_COMPLEX,0.6,(153,51,102),1)
            # Check if the person is yawning
            #if yawnStatus == True and prev_yawn_status == False:
                # play_alarm()
            # Update the previous yawn status
            prev_yawn_status = yawnStatus
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    webcamera.release()    


  


from tkinter import *
import tkinter

main = tkinter.Tk()
main.title("Driver Drowsiness Monitoring System")
main.geometry("800x500")
main.resizable(False, False)

# Professional color scheme
bg_color = '#f0f0f0'  # Light gray
text_color = '#333333'  # Dark gray
accent_color = '#4285F4'  # Google Blue

main.config(bg=bg_color)

# Title bar
font_title = ('calibri', 28, 'bold', 'underline')
title = Label(main, text='Driver Drowsiness Monitoring System', anchor=CENTER, justify=CENTER)
title.config(bg=bg_color, fg=accent_color, font=font_title)
title.config(height=2)
title.pack(fill=X, pady=(10, 0))

# Subtitle
font_subtitle = ('calibri', 18, 'italic')
subtitle = Label(main, text='Ensuring Safe Driving Through Advanced Technology', anchor=CENTER, justify=CENTER)
subtitle.config(bg=bg_color, fg=accent_color, font=font_subtitle)
subtitle.pack(fill=X, pady=(0, 10))

# GUI components and layout
font_button = ('calibri', 14, 'bold')
upload = Button(main, text="Start Monitoring", command=startMonitoring, bg=accent_color, fg='white')
upload.config(font=font_button)
upload.pack(pady=(20, 10))

status_label = Label(main, text="Webcam Status: Not Connecting...", bg=bg_color, fg=text_color, font=font_button)
status_label.pack()

info_label = Label(main, text="Monitor the driver's behavior for signs of drowsiness.", bg=bg_color, fg=text_color, font=('calibri', 12))
info_label.pack(pady=10)

# Additional feature: Toggle button
toggle_var = IntVar()
toggle_button = Checkbutton(main, text="Enable Advanced Monitoring", variable=toggle_var, bg=bg_color, fg=accent_color, font=font_button)
toggle_button.pack(pady=10)

pathlabel = Label(main, text="Path: /Drowsydriverdetection/python/windows C", bg=bg_color, fg=text_color, font=font_button)
pathlabel.pack()

credits_label = Label(main, text="Developed by Gayatri,Pallavi and Abhilash | Version 1.0", bg=bg_color, fg=text_color, font=('calibri', 10, 'italic'))
credits_label.pack(side=BOTTOM, fill=X, pady=(20, 0))

main.mainloop()
