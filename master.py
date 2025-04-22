#master file of CR
print("Hello I am CR!")
from net import is_con
from mech import rover,stepper
from detect import detect as dtf
import cv2 as cv
import pygame
import threading
import datetime as dt
import os
#global values
record_state=False
facedetection_state=False
face_align=[(0,0),(False,False)]

def main_cleanup():
    is_con.cleanup()
    rover.cleanup()
    stepper.cleanup()

def record():
    global record_state, facedetection_state, face_align
    scale_x=0.3
    scale_y=0.3

    web_cam = cv.VideoCapture(0)
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
    fps = 10.0  # Frames per second
    out = None  # Initialize VideoWriter object

    # Main loop to read frames from the camera and save them.
    while True:
        # Read a frame from the camera.  ret is True if the frame was read successfully.
        ret, frame = web_cam.read()

        if facedetection_state:
            dx,dy= dtf.loc_face(frame,frame_width,frame_height)
            x_dir= False if (dx>=0) else True
            y_dir= True if (dy>=0) else False
            dx= abs(round(dx))
            dy= abs(round(dy))
            #print(f"dx:{dx}, dy:{dy}")
            if dx<10:
                dx=0
                scale_x=0.3
            elif dx<50:
                scale_x=0.1
            else:
                scale_x=0.3
            if dy<10:
                dy=0
                scale_y=0.3
            elif dy<50:
                scale_y=0.1
            else:
                scale_y=0.3

            face_align[0]= (round(dx*scale_x), round(dy*scale_y))
            face_align[1]= (x_dir,y_dir)
            #dtf.loc_face(frame,frame_width,frame_height)

        if not ret:
            print("Error: Could not read frame.")
            break  # Exit the loop if we can't get a frame

        # Write the frame to the output video file.
        if record_state and out is not None:
            try:
                out.write(frame)
            except Exception as e:
                print(f"Error writing frame: {e}")
                record_state = False #stop recording on error
                if out is not None:
                    out.release()
                out = None
                print(f"Video recording stopped due to error.")

        # Display the captured frame in a window (optional, for preview).
        cv.imshow('Webcam Recording', frame)

        # Wait for a key press.  'q' to quit.
        keypress = cv.waitKey(1)
        if keypress & 0xFF == ord('q'):
            break
        elif keypress & 0xFF == ord('r'):
            record_state = not (record_state)
            if record_state:
                print("Recording started!")
                now = dt.datetime.now()
                f_datetime = now.strftime("%Y%m%d_%H%M%S")
                output_dir = r"/home/mpi/Videos"  # Use raw string for the directory
                output_file = os.path.join(output_dir, f"output_{f_datetime}.avi")
                print(f"Output file path: {output_file}")  # Print the absolute file path to help debug
                # Ensure the directory exists
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except Exception as e:
                    print(f"Error creating directory: {e}")
                    print(f"Directory not created: {output_dir}")
                    record_state = False # Stop recording.
                    out = None
                    continue # go to the next iteration of the loop
                try:
                    out = cv.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
                except Exception as e:
                    print(f"Error creating VideoWriter: {e}")
                    print(f"Could not create writer for {output_file}")
                    record_state = False #stop recording
                    out = None
                    continue #next iteration
            else:
                if out is not None:
                    out.release()
                print(f"Video saved as {output_file}")
                print("Recording stopped!")

    # Release the camera and the VideoWriter object.  Important to free resources.
    web_cam.release()
    if out is not None:
        out.release()  # Release only if it was initialized

    # Destroy all windows (optional, but good practice).
    cv.destroyAllWindows()

def joystick():
    global record_state, facedetection_state
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
    but_state=False
    axis=None
    value=0.0
    try:
        while True:
            # Get events to keep the system responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.JOYBUTTONDOWN:
                    but= event.button
                    but_state=True
                    #stepper.rot(but,True)
                    print(f"Button {but} pressed")

                elif event.type == pygame.JOYBUTTONUP:
                    but= event.button
                    but_state=False
                    #stepper.rot(but,False)
                    print(f"Button {but} released")
                elif event.type == pygame.JOYAXISMOTION:
                    axis = event.axis
                    value = event.value
                    #rover.moment(axis,value)
                    # print axis values, limit to 2 decimal places
                    print(f"Axis {axis} value: {value:.2f}")
                '''
                elif event.type == pygame.JOYHATMOTION:
                    hat = event.hat
                    value = event.value
                    print(f"Hat {hat} value: {value}")
                '''

                if record_state and facedetection_state and (but not in [4,5]):
                    pygame.time.delay(10)
                    continue #skips the gamepad input events when recording started and facedetection enabled
                if but ==5 and but_state:
                    facedetection_state = not(facedetection_state)
                #elif but == 5 and but_state:
                #    facedetection_state = not(facedetection_state)

            rover.moment(axis,value)
            if not(facedetection_state):
                stepper.rot(but,but_state)
            else:
                stepper.rot_xy(face_align[0][0],face_align[1][0])
                stepper.rot_yz(face_align[0][1],face_align[1][1])
            
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
    cam_thread= threading.Thread(target=record)
    cam_thread.daemon=True
    cam_thread.start()
    joystick()

main_cleanup()