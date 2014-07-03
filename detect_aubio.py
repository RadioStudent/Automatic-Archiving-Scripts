# Nick Masluk
# 2013-05-05

# directories to compare files between
# set to the same directory to compare files between themselves
dir = '/home/ubuntustudio2/Desktop/#makana#/new_test/'
filter_dir = '/home/ubuntustudio2/Desktop/#makana#/new_test/filter/'
output = '/home/ubuntustudio2/Desktop/#makana#/new_test/output/'
filter_name = '_filter.wav'

# report match when cross correlation has a peak exceeding threshold
threshold = '0.2'
silence = '-65'
onset = 'hfc'
hopsize = '128'


lowpass = 20998
highpass = 21002

################################################################################
# import modules
################################################################################

from pydub import AudioSegment

import os
import subprocess


import wave
import numpy as np


import re
import commands
import numpy
import math

################################################################################
# function definitions
################################################################################

# adds escape characters in front of Bash special characters
def esc_bash_chars(string):
    # match any of the following characters between the capital A's
    # A`!$^&*()=[]{}\|;:'",<>? A
    # note that characters ] and ' need escape characters themselves in the
    # regex, and \ requires two escape characters
    specialchars = re.compile('[`!$^&*()=[\]{}\\\|;:\'",<>? ]')
    string_escaped = ""
    for char in string:
        if specialchars.search(char):
            string_escaped += '\\' + char
        else:
            string_escaped += char
    return string_escaped


# write to a file
def write_string(string, filename):
    file_out = open(filename, 'ab')

    file_out.write(string)
    file_out.close()

def delete_string(string, filename):
    file_out = open(filename, 'wb')

    file_out.write(string)
    file_out.close()




################################################################################
# main code
################################################################################

# escape Bash special characters
dir = esc_bash_chars(dir)
filter_dir = esc_bash_chars(filter_dir)
output = esc_bash_chars(output)


working_dir = commands.getoutput('ls ' + dir + '*.wav').split('\n')
##print filelist_to_filter

for i, file in enumerate(working_dir):
    # if correlating between files within a directory, set filelist_b such that
    # cross-correlations are not repeated, and files are not correlated with
    # themselves
##    print i, file

    wr = wave.open(file , 'r')
    par = list(wr.getparams()) # Get the parameters from the input.

    par[3] = 0 


    ww = wave.open(file + filter_name, 'w')
    ww.setparams(tuple(par))


    sz = wr.getframerate()
    c = int(wr.getnframes()/sz)
    for num in range(c):
        print('Processing {}/{} s'.format(num+1, c))
        da = np.fromstring(wr.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2] # left and right channel
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter (1)
##        lf[55:66], rf[55:66] = 0, 0 # line noise filter (2)
        lf[highpass:], rf[highpass:] = 0,0 # high pass filter (3)
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
        ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
        ww.writeframes(ns.tostring())

    wr.close()
    ww.close()
##    subprocess.check_output('mv ' + file + filter_name + ' ' + filter_dir, shell=True)



    # calculate fingerprint
    fpcalc_out = subprocess.check_output('aubioonset -i ' + file  + filter_name + ' -t ' + threshold + ' -s ' + silence + ' -O ' + onset+ ' -H ' + hopsize, shell=True)
##    print fpcalc_out

    # Split string by new line character to make array of lines.
    lines = fpcalc_out.split("\n")
    print lines
    # Loop through array
    x = "0"
    y = "100000"
    for index, line in enumerate(lines):
    ##    print song.duration_seconds

    # Only print every second element.
##    if index % 2 == 0:
##        print "index:", index
##        print "line:", line
        
        # Print line in specified format.
        if line == "":
            line = y
##        if index % 2 == 0:
##            x = int(float(x)-10)
##            print x
##            print(x + "\t" + line + "\t" + str(index // 2 + 1))
        write_string((str(x) + "\t" + str(line) + "\t" + file + str(index) + "\n"), file + '.txt')
        x = line
    file_mp3 = file.replace(".wav", ".mp3")
##        print j, file_mp3, output
    subprocess.check_output('mp3splt ' + file_mp3 + ' -A ' + file + '.txt -d /' , shell=True)

##    delete_string("", file + '.txt')
##m = re.search(r"\n", fpcalc_out)
##print m

##fpcalc_out_1 = fpcalc_out[:m.start()] + "\t" + fpcalc_out[:m.start()] + "\t" + "a"  + "\n" + fpcalc_out[m.end():] + "\t" + fpcalc_out[m.end():] + "\t" + "b" + "\n"
##print fpcalc_out_1

##write_string(fpcalc_out_1, match_file)
