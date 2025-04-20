#master file of CR
print("Hello I am CR!")
from net import is_con
from mech import rover,stepper
import cv2 as cv

def main_cleanup():
    is_con.cleanup()
    rover.cleanup()
    stepper.cleanup()

def record():
    web_cam= cv.VideoCapture(0)
    if not web_cam.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Get the width and height of the video frames.  Important for VideoWriter.
    frame_width = int(web_cam.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(web_cam.get(cv.CAP_PROP_FRAME_HEIGHT))


    # Define the codec and create a VideoWriter object to save the video.
    # FourCC is a 4-character code specifying the video codec.
    # 'XVID' is a common codec; you can try others like 'MJPG', 'MP4V', or 'H264' (if available).
    fourcc = cv.VideoWriter_fourcc(*'XVID')  # Or try:  cv2.VideoWriter_fourcc(*'MJPG')
    output_file = 'output.avi'  # Name of the output video file
    fps = 30.0  # Frames per second
    out = cv.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    # Main loop to read frames from the camera and save them.
    while True:
        # Read a frame from the camera.  ret is True if the frame was read successfully.
        ret, frame = web_cam.read()

        if not ret:
            print("Error: Could not read frame.")
            break  # Exit the loop if we can't get a frame

        # Write the frame to the output video file.
        out.write(frame)

        # Display the captured frame in a window (optional, for preview).
        cv.imshow('Webcam Recording', frame)

        # Wait for a key press.  'q' to quit.
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and the VideoWriter object.  Important to free resources.
    web_cam.release()
    out.release()

    # Destroy all windows (optional, but good practice).
    cv.destroyAllWindows()

    print(f"Video saved as {output_file}")

