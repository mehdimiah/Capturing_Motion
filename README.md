# Capturing_Motion
This was my second project using open-cv2, I have created a script able to detect motion within the webcams view.

when using this, begin with a clear still background so opencv is able to create an idea of the room with 0 movement.

this is a very basic motion detector, therefore lighting and changes will effect the cameras ability to identify moving objects.

this program is great for a base script, i would add features such as saving all motion occurrances (which i began but i have only began implementing this)

motion when detected will be drawn around similar to face detection, i have also implemented text and datetime into the video capture.

there are two files, video grey is purely motion detection. 

however, plotting.py uses the bokeh library to takes the length of time motion is detected within the camera and create a html interactive graph plotting as a timeseries plot.

please note i used a usb webcam, you can change the camera used in the code at the video variable, it can be changed to 0,1 or 2 which refers to different cameras attached
to the computer.
