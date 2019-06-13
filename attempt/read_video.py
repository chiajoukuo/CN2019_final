import cv2
import sys
 
# (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
if __name__ == '__main__' :

    # Read video
    video = cv2.VideoCapture("MU_1.mp4")
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        # timer = cv2.getTickCount()

        # Calculate Frames per second (FPS)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Display FPS on frame
        # cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
        # print(frame)
        # cv2.imwrite("./MU_1/"+nname+".jpg", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break