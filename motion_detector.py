import cv2

first_frame = None # Variable to store the first frame for motion detection
video = cv2.VideoCapture(0) # Initialize video capture from the default camera

while True:
    check, frame = video.read() # Read a frame from the video capture

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame to grayscale
    gray = cv2.GaussianBlur(gray, (21, 21), 0) # Apply Gaussian blur to the grayscale frame for better motion detection
    
    if first_frame is None:
        first_frame = gray # Set the first frame if it is not set
        continue

    delta_frame = cv2.absdiff(first_frame, gray) # Compute the absolute difference between the first frame and the current frame
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] # Threshold the delta frame to get a binary image
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2) # Dilate the thresholded frame to fill in holes
    
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find contours in the thresholded frame

    for contour in cnts:
        if cv2.contourArea(contour) < 500: # Ignore small contours
            continue
        (x, y, w, h) = cv2.boundingRect(contour) # Get the bounding box for the contour
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) # Draw a rectangle around the detected motion

    cv2.imshow("Gray frame", gray) # Display the frame
    cv2.imshow("Delta Frame", delta_frame) # Display the delta frame
    cv2.imshow("Threshold Delta", thresh_frame) # Display the thresholded delta frame
    cv2.imshow("Color Frame", frame) # Display the original frame with motion rectangles

    key = cv2.waitKey(1) # Wait for a key press
    if key == ord('q'): # If 'q' is pressed, exit the loop
        break

video.release() # Release the video capture object
cv2.destroyAllWindows() # Close all OpenCV windows
