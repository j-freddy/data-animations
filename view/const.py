# Set to True during production
PROD = True
DIROUT = "out"
FILEOUT = "video.mp4"
# Local screen is too small for 1920x1080
GLOBAL_SCALE = 2 if PROD else 1

FPS = 60
FRAMES_PER_ENTRY = 2.5
WINDOW_W = 960
WINDOW_H = 540
