# Nick Masluk
# 2013-05-05

# directories to compare files between
# set to the same directory to compare files between themselves
dir_a = '/home/ubuntustudio2/Desktop/#makana#'
dir_b = '/home/ubuntustudio2/Desktop/#makana#'
# file to write matches to
match_file = '/home/ubuntustudio2/Desktop/#makana#/matches.txt'
# seconds to sample audio file for
sample_length = 500
# number of points to crop from beginning of fingerprint
# 4096 / 11025 Hz / 3 = 0.124 seconds per point
crop = 110
# number of points to scan cross correlation over
span = 1200
# step size (in points) of cross correlation
step = 3
# report match when cross correlation has a peak exceeding threshold
threshold = -10

################################################################################
# import modules
################################################################################
import os
import subprocess


import re
import commands
import numpy
import math

# write to a file
def write_string(string, filename):
    file_out = open(filename, 'ab')

    file_out.write(string)
    file_out.close()

def delete_string(string, filename):
    file_out = open(filename, 'wb')

    file_out.write(string)
    file_out.close()

# delete content of the file
delete_string("", match_file)

# calculate fingerprint
fpcalc_out = subprocess.check_output('aubiocut -i input_21Khz_f.wav -s -60', shell=True)
print fpcalc_out

# Split string by new line character to make array of lines.
lines = fpcalc_out.split("\n")
##print lines
# Loop through array
x = "0"
y = "10000000"
for index, line in enumerate(lines):

    # Only print every second element.
    if index % 2 == 0:
##        print "index:", index
##        print "line:", line
        # Print line in specified format.
        if line == "":
            line = y
        print(x + "\t" + line + "\t" + str(index // 2 + 1))
        write_string((x + "\t" + line + "\t" + str(index // 2 + 1) + "\n"), match_file)
        x = line

##m = re.search(r"\n", fpcalc_out)
##print m

##fpcalc_out_1 = fpcalc_out[:m.start()] + "\t" + fpcalc_out[:m.start()] + "\t" + "a"  + "\n" + fpcalc_out[m.end():] + "\t" + fpcalc_out[m.end():] + "\t" + "b" + "\n"
##print fpcalc_out_1

##write_string(fpcalc_out_1, match_file)
