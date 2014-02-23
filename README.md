eyetracking_alignment
=====================


This Python script can be used to align the onset of some stimulus (e.g., audio stimulus) to people's eye-fixations at that particular onset. Eye-movements within a certain time interval use by the user will be retained and data outside the interval will be removed. 

For example, suppose we ask participants' to listen to sentneces like "Person A said that Person B thought he could get into a good college." Suppose that we are interested in how people interpret the pronoun 'he'. As a result, we want to know participants' eye fixation patterns within the time interval starting 100 samples prior to the onset of the word "he" and ending 1000 samples after the onset of "he". In other words, we want to retain the data within this 1100 sample window and remove any data outside the time interval. Also, we want to set the sample at the onset of he as sample 0. Samples prior to the onset of "he" get negtaive sample indices and sample after the onset of "he" get positive indices (i.e., ...-4, -3, -2, -1, 0, 1, 2, 3, 4, 5,...). 

To accomplish this, we need to provide a file that includes the onset time of each sound file that participants listened to along with the unique name of each sound file (the name must also be in the raw eye tracking data in order to match the onset time with the eye tracking data. We also need to provide a raw eye tracking data file (in .txt format) and specify the number of samples needed prior and after the onset and the sample rate of the eye tracker - that is, the number of samples taken per second. 

