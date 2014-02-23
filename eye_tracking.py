################################################################################
#                                                                              #
#                  !!!!Only change ths section BELOW!!!                        #
#                                                                              #
################################################################################
#Some some information needed to process the file. Fill them or change them as needed:

#Name (including the file path if needed) of the raw eyetracking data file
file_name = "XiaoNov27_2012.txt"

#Name (including the file path if needed) of the time file needed for alignment
align_file_name = "eyetracking_align.txt"

#Name of the aligned output file:
output_file = "AlignedEyetrackingData.txt"

#Whether the time in the time file is in seconds: True = sec; False = ms:
seconds = True

#Name of the column in the time file that containing the alignment time:
align_var = "Verb_onset"

#Name of the column in the time file that identifies what you need to align (e.g., names of audio files):
time_align_var = "audio"

#Name of the column in the raw data file that identifies what you need to align (e.g., names of audio files):
raw_align_var = "audio"

#Audio delay time in SECONDS (the time between the onset of the displayed image and the onset of audio file)
audio_delay = 1

#Sample rate: i.e., the number of samples per second (or per 1000 milliseconds)
sample_rate = 500

#Number of samples prior to onset:
numsum_prior = 100

#Number of samples after onset:
numsum_post = 1000

################################################################################
#                                                                              #
#                  !!!!Only change ths section ABOVE!!!!                       #
#                                                                              #
################################################################################




 """
         __________    __________    __________    __________
        |  ________|  |____   ___|  |  ______  |  |  ______  |
        | |                | |      | |      | |  | |      | |
        | |________        | |      | |      | |  | |______| |
        |________  |       | |      | |      | |  |  ________| 
                 | |       | |      | |      | |  | |
         ________| |       | |      | |______| |  | |
        |__________|       |_|      |__________|  |_|

              !!!!DO NOT change ths section below!!!! 

 """
import align_main as align
align.align_output( file_name, align_file_name, seconds, align_var, time_align_var, raw_align_var, audio_delay, sample_rate, numsum_prior, numsum_post, output_file )





