#master file of CR
print("Hello I am CR!")
from net import is_con
from mech import rover,stepper
import cv2 as cv
import pygame
import threading
import datetime as dt

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
    record_state=False

    # Main loop to read frames from the camera and save them.
    while True:
        # Read a frame from the camera.  ret is True if the frame was read successfully.
        ret, frame = web_cam.read()

        if not ret:
            print("Error: Could not read frame.")
            break  # Exit the loop if we can't get a frame

        # Write the frame to the output video file.
        if (record_state):
            out.write(frame)

        # Display the captured frame in a window (optional, for preview).
        cv.imshow('Webcam Recording', frame)

        # Wait for a key press.  'q' to quit.
        keypress=cv.waitKey(1)
        if keypress & 0xFF == ord('q'):
            break
        elif keypress & 0xFF == ord('r'):
            record_state != record_state
            if(record_state):
                print("Recording started!")
            else:
                out.release()
                print("Recording stopped!")

    # Release the camera and the VideoWriter object.  Important to free resources.
    web_cam.release()
    out.release()

    # Destroy all windows (optional, but good practice).
    cv.destroyAllWindows()

    print(f"Video saved as {output_file}")

def joystick():
    """
    Initializes pygame, reads gamepad input, and prints button and axis values.
    """
    pygame.init()
    pygame.joystick.init()

    # Check for the number of connected joysticks
    if pygame.joystick.get_count() == 0:
        print("No gamepads detected. Please connect a gamepad and try again.")
        pygame.quit()
        return

    # Initialize the first gamepad (index 0)
    gamepad = pygame.joystick.Joystick(0)
    gamepad.init()
    but=0
    try:
        while True:
            # Get events to keep the system responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.JOYBUTTONDOWN:
                    but= event.button
                    stepper.rot(but,True)
                    print(f"Button {but} pressed")

                elif event.type == pygame.JOYBUTTONUP:
                    but= event.button
                    stepper.rot(but,False)
                    print(f"Button {but} released")
                elif event.type == pygame.JOYAXISMOTION:
                    axis = event.axis
                    value = event.value
                    rover.moment(axis,value)
                    # print axis values, limit to 2 decimal places
                    print(f"Axis {axis} value: {value:.2f}")
                '''
                elif event.type == pygame.JOYHATMOTION:
                    hat = event.hat
                    value = event.value
                    print(f"Hat {hat} value: {value}")
                '''

            # print("tick") # uncomment to see how often the loop runs.
            pygame.time.delay(10)  # Add a small delay to reduce CPU usage. 10milliseconds

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    indi_thread= threading.Thread(target=is_con.indicate)
    indi_thread.daemon=True #set the thread as daemon thus this thread exits automatically when main thread exits
    indi_thread.start()
    joy_thread= threading.Thread(target=joystick)
    joy_thread.daemon=True
    joy_thread.start()
    cam_thread= threading.Thread(target=record)
    cam_thread.daemon=True
    cam_thread.start()

main_cleanup()