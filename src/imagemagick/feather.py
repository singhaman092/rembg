import cv2
import numpy
import os
import sys

path = str(sys.argv[1])
cmd = (sys.argv[2])

outputh_path = ''

print(path, cmd)

# read image
img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
#os.system('convert image.png -alpha set -virtual-pixel transparent -channel A -morphology Distance Euclidean:1,50\! +channel tmp.png')
command = 'magick ' + path + \
    '-alpha set -set option:wd "%w" -set option:ht "%h" -set option:ht2 "%[fx:round(0.05*ht)]" -set \
         option:ht3 "%[fx:ht-ht2]" \( -size "%[wd]x%[ht3]" xc:white \) \( -size "%[wd]x%[ht2]" gradient:white-black \) \
             \( -clone 1,2 -append \) -delete 1,2 \( -clone 0 -alpha extract \) \( -clone 1,2 -compose multiply -composite \) \
             -delete 1,2 -alpha off -compose copy_opacity -composite '+ output_path
print(command)

# os.system(command)
# mask = cv2.imread('tmp.png', cv2.IMREAD_UNCHANGED)
# os.system('rm tmp.png')