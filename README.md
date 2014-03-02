###Eyetracking data alignment and cleaning
=====================


This Python script searches for a user-specified time point of interest (e.g., onset/offset time of a pronoun) in an audio stimulus on an experimental trial, and extracts a user-specified number of samples prior to and following the user-specified time point. Each sample also gets an index: the sample at the time point of interest has an index of 0, all the samples following the time point of interest get positive indices, and all the samples preceding the time point of interest getting negative indices (..., -4, -3, -2, -1, 0, 1, 2, 3, 4,...):



###Example
Suppose we ask participants to listen to sentences in the form of **"X verb-ed Y [in some place] because he ..."** while looking at corresponding pictures on a computer monitor. For example, one possible sentnece is ***John scolded Bill at the airport because he did not bring the passport***, and its corresponding picture is shown below.

![](http://imagizer.imageshack.us/v2/640x480q90/28/zcyj.png)

Furhter suppose that we are interested in how people interpret the pronoun ***he*** in real-time (of course, in a real experiment, both ***he*** and ***she*** would be used). One possibility is that we can examine comprehenders' eye fixation patterns from 200ms *prior* to the onset of ***he*** up to 2000ms *after* the onset of ***he***. In other words, we would like to extract the eye fixation data within a 2200ms time window on each trial.

Since each trial has a different sentence stimulus and hence a different recording, the onset time for the pronoun ***he*** is different from trial to trial. We need to have a text file that contains names that can uniquely identify the trials in the raw eye tracking data set and also contain the time points of interest (e.g., pronoun onset time) for the corresponding trials. In this example, the file name of each audio recording can be used as a unique identifier (see an exerpt below). Presumably, the file names should be present in the raw eye-tracking data file.


Audio | Pronoun_onset |
---|---|
Target_L1_1.wav | 1.714635598 
Target_L1_10.wav | 	2.069305375
Target_L1_11.wav | 	1.989329697
Target_L1_12.wav | 	2.373784056
Target_L1_13.wav | 	1.900261581
Target_L1_14.wav | 	2.092761663
Target_L1_15.wav | 	2.13880722
Target_L1_16.wav | 	2.018276529
Target_L1_17.wav | 	2.009345997
Target_L1_18.wav | 	2.161914031

We then need to specify the following variables in the `eye_tracking.py` file:

* The name of the raw data file (including the file path if needed): 

    `file_name = "raw_data_file.txt"`

* The name of the time file needed for alignment (including the file path if needed):
 
    `align_file_name = "pronoun_onset.txt"`

* The name of the aligned output file:

    `output_file = "aligned_output_file.txt"`

* Whether the time in the time file is in seconds: True = sec; False = ms:

    `seconds = True`

* The name of the column in the time file that containing the times of interest:

    `align_var = "Pronoun_onset"`

* The name of the column in the time file that uniquely identifies what you need to align (e.g., names of audio files):

    `time_align_var = "Audio"`

* The name of the column in the raw data file that uniquely identifies what you need to align (e.g., names of audio files):

    `raw_align_var = "audio"`

* Audio delay time in SECONDS (user-specified time between the onset of the displayed image and the onset of the audio file):

     `audio_delay = 1`

* Sample rate: i.e., the number of samples per second (or per 1000 milliseconds). It varies from eye-tracker to eye-tracker. For Eyelink-1000, the sampling rate is 500 samples per second. In other words, a sample is recorded for each 2 milliseconds:

     `sample_rate = 500`

* Number of samples prior to onset. In this example, we want to retain data starting 200ms *prior* to the pronoun onset. This is equivalent to 100 samples prior to the pronoun onset (2ms per sample, 200ms per 100 samples):

     `numsum_prior = 100`

* Number of samples after onset. In this example, we want to retain data up to 2000ms after the pronoun onset. This is equivalent to 1000 samples after the onset of pronoun (2ms per sample, 2000ms per 1000 samples):

     `numsum_post = 1000`

* Whether samples taken during eye blinks or saccades should be removed. If they are to be removed, the names of the columns from the raw eye tracking data set that contain the blink and saccade information should be specified as shown below:

     `blinksaccade_rm = ["RIGHT_IN_BLINK", "RIGHT_IN_SACCADE"]`

* this argument can be left empty if samples taken during blinking and saccades are not to be removed:

     `blinksaccade_rm = []`

* Interest area coordinate variables in the alignment file. Should be in the format of `x1, y1, x2, y2` - e.g., `70,25,320,743`.

     `interest_coords = ["Left2", "Middle2", "Right2"]`


Executing `eye_tracking.py` file will produce an output file that contains only data points (samples) within the time window of interest (e.g., in the example here, 200ms prior to pronoun onset to 2000ms after pronoun onset). 


###The functionality of identifying whether an eye fixation is inside an interest region has been added.




