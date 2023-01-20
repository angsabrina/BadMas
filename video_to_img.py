import cv2
import os 
import sys
import numpy as np
from datetime import time, timedelta

# the purpose of this script is to extract frames from an mp4 video to img files for training 

# code in this file is adapted from:
# https://pythonguides.com/read-video-frames-in-python/ 
# https://www.thepythoncode.com/article/extract-frames-from-videos-in-python

# number of frames saved per second of video
SAVING_FRAMES_PER_SECOND = 60

def format_timedelta(td):
    # utility function to format timedelta objects
    # from this: 12:42:06.901238 
    # to like so: (12:42:06)
    # ommitting microseconds and milliseconds since we are taking 1 frame per second

    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError: 
        print("Error in attempting to format_timedelta")
    return result.replace(":", "-")

def get_saving_frames_durations(cap, saving_fps):
    # function that returns the list of durations where to save the frames
    s = []

    # get clip duration by dividing number of frames by number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # np.arange() makes floating point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def main(video_file):
    # main function that calls OpenCV to parse the mp4 video file
    # outputs the image files in director ./images 

    # create images filedir if doesn't exist
    try:  
        if not os.path.exists('./data/images'): 
            os.makedirs('./data/images') 
    except OSError: 
        print ('Error')

    video = cv2.VideoCapture(video_file)
    # gets FPS of the video
    fps = video.get(cv2.CAP_PROP_FPS) 

    # if SAVING_FRAMES_PER_SECOND is above video fps, set it to FPS (as max)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    
    # get list of duration spots to save
    saving_frames_duration = get_saving_frames_durations(video, saving_frames_per_second)
    
    currentframe = 0

    # parse through video frames
    while(True): 
        ret, frame = video.read()
        
        # if current frame has been read
        if ret:
            frame_duration = currentframe / fps

            try:
                closest_duration = saving_frames_duration[0]
            except IndexError:
                # the list is empty, all duration frames were saved
                break

            if frame_duration >= closest_duration:
                # if closest frame time is less than equal to frame duration that we want, save the frame 
                saveFrame = timedelta(seconds=frame_duration)
                # write each frame as 'img*' where * is frame no.
                # name = './data/images/img' + str(int(saveFrame.seconds)) + '.jpg'
                if(currentframe % 2 != 0 and currentframe % 3 == 0):
                    name = './data/images/img' + str(int(currentframe)) + '.jpg'
                    print ('Captured...' + name)
                    cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break

    video.release() 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # takes in argument for video folder loc
    video_file = sys.argv[1]
    main(video_file)