import sys
import string

def data_process( dataset ):
  data = list()
  for line in dataset:
    data.append( line.split('\t') )
  return data


#Convert a data point to floating point in an eye-tracking dataset. Mainly used in
#cases where raw eye-tracking data represent numbers using quotation marks - e.g., "2.31236"
def Float(dataset, col_index):
  length = len(dataset)
  for i in range(length):
    dataset[i][col_index] = float( dataset[i][col_index] )
  return dataset

#Convert a data point to integer in an eye-tracking dataset. Mainly used in
#cases where raw eye-tracking data represent numbers using quotation marks - e.g., "3"
def Int(dataset, col_index):
  length = len(dataset)
  for i in range(length):
    dataset[i][col_index] = int( dataset[i][col_index] )
  return dataset


def time_convert(dataset, col_index, rate):
  length = len(dataset)
  for i in range(length):
    dataset[i][col_index] = dataset[i][col_index] * rate
  return dataset

#match the onset time (time point of interest) of a given trial
def match_onset(pattern, headers_align, align_file, align_var, time_align_var):
  align_ind = headers_align.index( align_var )
  search_ind = headers_align.index( time_align_var )
  output = 0
  for line in align_file:
    if line[search_ind] == pattern:
      output = line[align_ind]
  return output

#Removes tabs in a dataset.
def tab_remover(dataset):
  newset = list()
  for line in dataset:
    newset.append( line.split('\t') )
  return newset

#Remove samples taken during blinking and/or saccades:
def blinksaccade_remover(dataset, var_list, headers):
  length = len(headers)
  index = list()
  for item in var_list:
    for i in range(length):
      if item == headers[i]:
        index.append(i)
  newdata = list()
  length = len(dataset)
  for item in dataset:
    if '1' not in [item[i] for i in index ]:
      newdata.append( item )
  return newdata


#Search for the sample that was taken at a time point of interest. E.g., if we are interested
#in comprehenders' interpretation of the pronoun "he" in a recorded sentence, this function
#will look for the sample at the onset time of "he" in the recorded sentence, and produces
#the index for this sample. The index is the sample index on a given trial.
def scan(dataset, align_file, headers, headers_align, align_var, time_align_var, 
raw_align_var, audio_delay, time_per_samp):
  start = 0
  index = 0
  index_start = 0
  msg_index = headers.index("SAMPLE_MESSAGE")
  ind_index = headers.index("SAMPLE_INDEX")
  search_index = headers.index(raw_align_var)
  length = len(dataset)
  counter = 0
  indzero = list()
  for i in range(length):
    if dataset[i][msg_index] == "Variable_reset":
      set0 = match_onset( dataset[i][search_index], headers_align, align_file, align_var, time_align_var)
      start = 1
    elif dataset[i][msg_index] == "Click_screen_start" and start == 1:
      start = 2
      index = dataset[i][ind_index] 
      index_start = dataset[i][ind_index] 
    elif start == 2 and index < (audio_delay + index_start):
      index = dataset[i][ind_index] 
    elif start == 2 and index >= (audio_delay + index_start) and counter < (set0*1.0/time_per_samp):
      index = dataset[i][ind_index] 
      counter += 1
    elif start == 2 and index >= (audio_delay + index_start) and counter >= (set0*1.0/time_per_samp):
      indzero.append(i)
      start = 3
      counter = 0
  return indzero


#Looks for the index of the first sample to be retained and the index of the last sample to be 
#retained on a trial.
def bound_search(dataset, indzero, numsum_prior, numsum_post, align_col):
  bounds = dict()
  rowmax = len(dataset)
  for i in indzero:
    file_name = dataset[i][align_col]
    for j in range(i - 1, i - numsum_prior - 1, -1):
      if j == 0:
        bounds.get(i).append(j)
        break
      elif file_name != dataset[j][align_col]:
        bounds[i] = [j + 1]
        break
      elif j == (i - numsum_prior):
        bounds[i] = [j]
    for j in range(i, i + numsum_post + 1, 1):
      if j == (rowmax -1 ):
        bounds.get(i).append(j)
        break
      elif file_name != dataset[j][align_col]:
        bounds.get(i).append(j - 1)
        break
      elif j == (i + numsum_post):
        bounds.get(i).append( j )
  return bounds

"""
#The indices of all the samples between the first sample and the last sample to be retained on a trial
def align(dataset, numsum_prior, numsum_post, indzero):
  id_keep = []
  for i in indzero:
    id_keep = id_keep + range(i - numsum_prior, i, 1) + range(i, numsum_post + 1, 1)
  return id_keep
"""

#This function reduces the eye-tracking dataset by removing samples outside the time window of interest.
def reduce(dataset, bounds, indzero):
  newset = list()
  counter = 1
  for i in indzero:
    item = list()
    lo, hi = bounds.get(i)
    align_ind = 0
    for j in range(i-1, lo-1, -1):
      align_ind -= 1
      temp = dataset[j][:]
      temp.append(align_ind)
      item.insert(0, temp)
    align_ind = 0
    for j in range(i, hi+1, 1):
      temp = dataset[j][:]
      temp.append(align_ind)
      item.append(temp)
      align_ind += 1
    newset = newset + item
    counter += 1
  return newset


#Write the new dataset to a tab-delimited text file
def output(dataset, headers, file_name):
  file = open(file_name, "w")
  for i in range(len(headers)-1):
    file.write("%s\t" % headers[i])
  file.write("%s" % headers[len(headers)-1])
  for line in dataset:
    for i in range(len(headers)-1):
      file.write("%s\t" % line[i])
    file.write("%s" % line[len(headers)-1])
  file.close()

#Determine whether a fixation lands inside a target/interest area (on the monitor). 
#The output consists of 1s and 0s - 1 = inside the target area, 0 = outside.
def interest(dataset, headers, fixation_x, fixation_y, align_file, 
headers_align, interest_coord_vars, raw_align_var, time_align_var):
  xind, yind = headers.index( fixation_x ), headers.index( fixation_y )
  interest_ind = [ headers_align.index(i) for i in interest_coord_vars ]
  num_interest = len( interest_ind )
  output = [ [] for i in range(num_interest) ]
  raw_align_ind, align_ind = headers.index( raw_align_var), headers_align.index( time_align_var )
  table = string.maketrans("","")
  for line in dataset:
	tempind = [line[ raw_align_ind ] == item[ align_ind ] for item in align_file ].index(True)
	for i in range(num_interest):
		temp = align_file[ tempind ][interest_ind[i]]
		temp = [ coord.strip() for coord in temp.split(",") ]
		temp = [ coord.translate( table, string.punctuation ) for coord in temp ]
		temp = [ float(number) for number in temp ]
		temp = [ (temp[0], temp[1]), (temp[0], temp[3]), (temp[2], temp[1]), (temp[2], temp[3]) ]
		temp = fixation_in_area( float( line[ xind ] ), float( line[ yind ] ), temp)
		output[i].append( temp )
		if temp == 1 and i < (num_interest - 1):
			for j in range(i + 1, num_interest, 1):
				output[j].append( 0 )
			break
  return output
  

#This function is used by interest() and it determines whether a point is inside a polygon.
def fixation_in_area(x, y, interest_coordinates):
    n = len(interest_coordinates)
    IN = False
    x1, y1 = interest_coordinates[0]
    for i in range( n + 1 ):
        x2, y2 = interest_coordinates[i % n]
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        val = (y - y1)*(x2 - x1)/(y2 - y1) + x1
                    if x1 == x2 or x <= val:
                        IN = not IN
        x1, y1 = x2, y2
    return 1 if IN else 0
