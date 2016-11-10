import glob


# control marker consist of semantically normal and abnormal sentences also manipulated on carefull causal pronounciation
#change marker id to reflect these four conditions and precize item

def get_fn():
	# load maltes log and vmrk files 
	log_dir = '/vol/tensusers/mbentum/MALTE_CH4_eeg/log_files/'
	vmrk_dir = '/vol/tensusers/mbentum/MALTE_CH4_eeg/PyCorder_files_pp01-pp10/'

	fn_log = glob.glob(log_dir + '*.log')
	fn_vmrk = glob.glob(vmrk_dir + '*.vmrk')
	return fn_log,fn_vmrk

def open_log(f):
	# loads log file
	return [line.split('\t') for line in open(f).read().split('\r\n') if len(line.split('\t')) >= 8]

def open_vmrk(f):
	# load vmrk file
	return [line.split(',') for line in open(f).read().split('\r\n')]

def find_control(log):
	# obsolete
	return [line for line in log if len(line) >= 6 and 'control' in line[5]]

def n2marker(n,s):
	# creates marker based on vmrk style LETTER (spaces) number total length is four filled up with spaces
	n = str(n)
	assert len(n) <= 3
	nspace = 3 - len(n)
	return s + ' ' * nspace + n

def find_vmrk_line(vmrk_index,vmrk,mid,tid,trial_info):
	# takes vrmk mid (to find correct line) tid (to make marker unique) and trial_info to enrich marker info
	# enriches the vmrk lines based on log data
	# vmrk_index is obsolete and function is confusing
	found = False
 	for i,line in enumerate(vmrk):
		if not found:
			print mid,line
		if line[0][:2] == 'Mk' and line[1] == mid:
			temp = [line[1] , tid ] + trial_info
			line[1] = '_'.join(temp) 
			vmrk_index = i
			found = True
			break
	assert found
	return vmrk,vmrk_index
		
def link_log_vmrk(flog,fvmrk):
	# takes filename of log and vmrk file and links the log data of the trials to the vmrk markers and enriches the markers
	print flog,fvmrk

	print flog.split('/')[-1].split('.')[0] , fvmrk.split('/')[-1].split('.')[0]
	assert flog.split('/')[-1].split('.')[0] == fvmrk.split('/')[-1].split('.')[0]
	log,vmrk = open_log(flog),open_vmrk(fvmrk)
	vmrk_index = 0
	for line in log[1:]: # skip header
		if line[5] == 'question':
			print line,'000000000000000'
			continue
		trialn = line[4]
		gender = line[5].split('_')[2][-1]
		speech_style = line[5].split('_')[3]
		condition = line[5].split('_')[4]
		trial_type = line[5].split('_')[1]
		itemn = line[5].split('_')[0]
		word1 = line[5].split('_')[5]
		word2 = line[5].split('_')[6].split('.')[0]
		trial_info = [gender,speech_style,condition,trial_type,itemn,word1,word2]
		marker_id_sentence = str(int(line[6]) - 1)
		marker_id_adjective = str(int(line[7])-1)
		marker_id_noun = line[8]
		mid = [marker_id_sentence,marker_id_adjective,marker_id_noun]
		marker_type = 'sentence,adjective,noun'.split(',')
		if mid[1] == mid[2]:
			mid.pop(1)
			marker_type.pop(1)
		for i,m in enumerate(mid):
			if i == 0:
				trial_info.append(marker_type[i])
			else:
				trial_info[-1] = marker_type[i]
			vmrk,vmrk_index = find_vmrk_line(vmrk_index,vmrk,n2marker(m,'S'),trialn,trial_info)
			print vmrk_index,trialn
	return vmrk 
		

def add_milli2vmrk(vmrk):
	#assumes sf of 500 Hz calcs time since start in millis
	output = []
	for line in vmrk:
		temp = line[:]
		if line[0][:2] == 'Mk':
			temp.append(str(int(line[2])*2))
		output.append(temp)
	return output


def time_since_last_marker(vmrk):
	# assumes sf of 500Hz calcs time since last marker
	output = []
	for i,line in enumerate(vmrk):
		temp = line[:]
		if line[0][:2] == 'Mk' and vmrk[i-1][0][:2] == 'Mk':
			temp.append(str((int(line[2]) - int(vmrk[i-1][2]))*2))
		output.append(temp)
	return output



