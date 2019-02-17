#/usr/bin/python3

import subprocess

#capture webcam image and save it
subprocess.call('fswebcam -d /dev/video1 myfood.jpg', shell=True)

