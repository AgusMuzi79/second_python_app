import cv2
from datetime import datetime
import pandas as pd

first_frame = None # Variable to store the first frame for motion detection
video = cv2.VideoCapture(0) # Initialize video capture from the default camera
status_list = [None, None] # List to keep track of motion status
times = [] # List to keep track of timestamps of motion events
df = pd.DataFrame(columns=["Start", "End"]) # DataFrame to store start and end times of motion events

while True:
    check, frame = video.read() # Read a frame from the video capture
    status = 0 # Initialize status variable

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
        if cv2.contourArea(contour) < 250: # Ignore small contours
            continue
        status = 1 # Set status to 1 if a significant contour is found
        (x, y, w, h) = cv2.boundingRect(contour) # Get the bounding box for the contour
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) # Draw a rectangle around the detected motion
    status_list.append(status) # Append the current status to the status list


    if status_list[-1] == 1 and status_list[-2] == 0: # Check for motion start
        times.append(datetime.now()) # Record the time when motion starts
    if status_list[-1] == 0 and status_list[-2] == 1: # Check for motion end
        times.append(datetime.now()) # Record the time when motion ends


    cv2.imshow("Gray frame", gray) # Display the frame
    cv2.imshow("Delta Frame", delta_frame) # Display the delta frame
    cv2.imshow("Threshold Delta", thresh_frame) # Display the thresholded delta frame
    cv2.imshow("Color Frame", frame) # Display the original frame with motion rectangles

    key = cv2.waitKey(1) # Wait for a key press
    if key == ord('q'): # If 'q' is pressed, exit the loop
        if status == 1: # If motion was active when quitting
            times.append(datetime.now()) # Record the time when motion ends if it was active
        break


print(status_list) # Print the status list to the console
print(times) # Print the times of motion events to the console

for i in range(0, len(times), 2): # Iterate through the times list in pairs
    df.loc[len(df)] = {"Start": times[i], "End": times[i + 1]} # Append start and end times to the DataFrame

df.to_csv("Times.csv") # Save the DataFrame to a CSV file
video.release() # Release the video capture object
cv2.destroyAllWindows() # Close all OpenCV windows
