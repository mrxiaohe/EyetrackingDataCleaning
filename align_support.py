import sys

def data_process( dataset ):
  data = list()
  for line in dataset:
    data.append( line.split('\t') )
  return data

def Float(dataset, col_index):
  length = len(dataset)
  for i in range(length):
    dataset[i][col_index] = float( dataset[i][col_index] )
  return dataset

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

def match_onset(pattern, headers_align, align_file, align_var, time_align_var):
  align_ind = headers_align.index( align_var )
  search_ind = headers_align.index( time_align_var )
  output = 0
  for line in align_file:
    if line[search_ind] == pattern:
      output = line[align_ind]
  return output

def tab_remover(dataset):
  newset = list()
  for line in dataset:
    newset.append( line.split('\t') )
  return newset


def scan(dataset, align_file, headers, headers_align, align_var, time_align_var, raw_align_var, audio_delay):
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
    elif start == 2 and index >= (audio_delay + index_start) and counter < (set0/2):
      index = dataset[i][ind_index] 
      counter += 1
    elif start == 2 and index >= (audio_delay + index_start) and counter >= (set0/2):
      indzero.append(i)
      start = 3
      counter = 0
  return indzero


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

def align(dataset, numsum_prior, numsum_post, indzero):
  id_keep = []
  for i in indzero:
    id_keep = id_keep + range(i - numsum_prior, i, 1) + range(i, numsum_post + 1, 1)
  return id_keep

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

def output(dataset, headers, file_name):
  file = open(file_name, "w")
  for i in range(len(headers)):
    file.write("%s\t" % headers[i])
  file.write("align")
  for line in dataset:
    for i in range(len(headers)):
      file.write("%s\t" % line[i])
    file.write("%s" % line[len(headers)])
  file.close()

def blinksaccade_remover(dataset, var_list, headers):
  length = len(headers)
  index = list()
  for item in var:
    for i in range(length):
      if item == headers[i]:
        index.append(i)
  newdata = list()
  length = len(dataset)
  for item in dataset:
    if '1' not in [item[i] for i in index ]:
      newdata.append( item )
  return newdata

