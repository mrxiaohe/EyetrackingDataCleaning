import align_support as support

def align_output(  file_name, align_file_name, seconds, align_var, time_align_var, 
raw_align_var, audio_delay, sample_rate, numsum_prior, numsum_post, output_file, 
blinksaccade_rm, interest_coords, fixation_x="RIGHT_GAZE_X", fixation_y="RIGHT_GAZE_Y"):
	data = open(file_name).read().strip().split('\r')
	data = support.tab_remover( data )
	align_file = open(align_file_name).read().strip().split('\r')
	align_file = support.tab_remover( align_file )
	headers = data[0]
	headers_align = align_file[0]
	samp_msg_ind, samp_ind = headers.index("SAMPLE_MESSAGE"), headers.index("SAMPLE_INDEX") 
	align_var_ind = headers_align.index(align_var)
	align_raw_var_ind = headers.index(raw_align_var)
	del data[0] 
	del align_file[0]
	timeMultiple = 1000 if seconds else 1
	audio_delay = audio_delay*sample_rate
	data = support.Int( data, samp_ind )
	time_per_samp = 1000*1.0/sample_rate
	align_file = support.time_convert( support.Float( align_file, align_var_ind ), align_var_ind , timeMultiple )
	indzero = support.scan(data, align_file, headers, headers_align, align_var, time_align_var, raw_align_var, audio_delay, time_per_samp)
	bounds = support.bound_search(data, indzero, numsum_prior, numsum_post, align_raw_var_ind)
	newset = support.reduce(data, bounds, indzero)
	headers = headers + ["align"]
	if blinksaccade_rm:
		newset = support.blinksaccade_remover(newset, blinksaccade_rm, headers)
	if interest_coords and not blinksaccade_rm:
		print("Samples taken during blinks and saccades must be removed in \norder tocheck whether a fixation lands inside an interest area")
	elif interest_coords and blinksaccade_rm:
		target = support.interest(newset, headers, fixation_y, fixation_y, align_file, headers_align, interest_coords, raw_align_var, time_align_var)
		headers = headers + ["YN_" + item for item in interest_coords]
		for i in range(len(newset)):
			for item in target:
				newset[i].append( item[i] ) 
	support.output(newset, headers, output_file)
