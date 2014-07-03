from pydub import AudioSegment
import re
import commands

dir_a = '/home/ubuntustudio2/Desktop/#makana#/U_with_21khz/AVIZZO/'
dir_b = '/home/ubuntustudio2/Desktop/#makana#/U_with_21khz/21khz/'

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
            string_escaped += '' + char
        else:
            string_escaped += char
    return string_escaped


# escape Bash special characters
dir_a = esc_bash_chars(dir_a)
dir_b = esc_bash_chars(dir_b)


# get list of files to compare from each directory
filelist_a = commands.getoutput('ls ' + dir_a + '*.mp3').split('\n')
filelist_b = commands.getoutput('ls ' + dir_b + '*.wav').split('\n')
##print filelist_a
##print filelist_b


# if cross-correlating between files within a directory, don't correlate files
# twice, or correlate files with themselves
intra_correlating = False
if filelist_a == filelist_b:
    intra_correlating = True

for i, file in enumerate(filelist_a):
    # if correlating between files within a directory, set filelist_b such that
    # cross-correlations are not repeated, and files are not correlated with
    # themselves
    if intra_correlating:
        # remove files already correlated with from filelist_b, along with
        # current file
        filelist_b = filelist_a[i+1:]
        if len(filelist_b) == 0:
            # nothing left to check!
            break
    print i, file
    file = esc_bash_chars(file)
    print file


    sound1 = AudioSegment.from_mp3(file)
    print sound1
    print sound1.duration_seconds
    sound2 = AudioSegment.from_wav("/home/ubuntustudio2/Desktop/#makana#/U_with_21khz/21khz/21Khz_sample.wav")


    # mix sound2 with sound1, starting at 5000ms into sound1)
##    output = sound1.overlay(sound2, position=(sound1.duration_seconds - 750))
##    output = sound1.overlay(sound2, position=(sound1.duration_seconds - 0500))
    output = sound1.overlay(sound2, position=0300)
    
    # save the result
    file = file.replace(".mp3", " 21khz.flac")
    output.export( file, format="flac")
##song = AudioSegment.from_wav(file_a)

# Split string by new line character to make array of lines.
##lines = fpcalc_out.split("\n")
##print lines
# Loop through array
##x = "0"
##y = song.duration_seconds
##print song.duration_seconds
