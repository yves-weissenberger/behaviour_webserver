from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
#________________
from django.utils.timezone import utc
import datetime


#________________
import os, errno
import csv
import os
import re
import ast
import subprocess
from multiprocessing.dummy import Pool
import zipfile


#________________________________________________________________________________________________________








def boxes(request):
 	numBoxes = get_num_boxes()

	box_connected = ping_boxes(numBoxes)


	mouseIDs = [get_mouse_ID(box_nr) for box_nr in range(numBoxes)]
	
	context = {'boxs_and_IDs':zip(range(numBoxes), mouseIDs,box_connected)}
	#context = {'box_list': range(numBoxes),'mouseIDs':mouseIDso
	# ideally, we want to expand this bit to include which
	# which mouse is in there and what task it is performing
	# add this as things to the context thing
	return render(request,'getData/boxes.html',context)


def box_info(request, box_nr):

	box_connected = ping_box(box_nr)
	#box_connected = is_online=='True'
	mouse_ID = get_mouse_ID(box_nr)

	task_schedule = get_mouse_task_schedule(box_nr)

	try:
		tasks, durations,duration_str = parse_task_schedule(task_schedule)



	except:
		tasks = []
		durations = []
		duration_str = []



	try:
		time_received = datetime.datetime.strptime(  re.findall(r'.*received(.*)',task_schedule)[0] , '%Y-%m-%d %H:%M:%S.%f')
		time_elapsed_tdelta = datetime.datetime.now() - time_received
		time_elapsed = time_parser( time_elapsed_tdelta.total_seconds() )
		
		cumsum_TL = []
		acc = 0
		for i in durations:
	    		acc += 1
	    		cumsum_TL.append(acc)
			task_completions = [time_elapsed_tdelta.total_seconds()>i for i in cumsum_TL]
		
	except IndexError:
		time_received = 'Not accessed yet'
		time_elapsed = []
	if len(tasks)==1:
		task_completions = [False]
		total_dur = time_parser(durations[0])
	else:
		task_completions = [i<-1 for i in range(len(tasks))]
		total_dur = time_parser(sum(durations))
		






	context = {'box_nr': box_nr,'mouse_ID':mouse_ID,
		   'task_names_and_durations': zip(tasks,duration_str,task_completions),
		   'total_duration': total_dur,
		   'time_elapsed': time_elapsed,
		   'isOnline':box_connected}


	return render(request,'getData/box_info.html',context)



#________________________________________________________________________________________________________
def set_mouse_ID(request,box_nr):
	
	context = {'box_nr': box_nr}
	return render(request, 'getData/set_mouse_ID.html',context)

	
def write_mouse_ID(request,box_nr):

	openstr = '/home/rastamouse/Documents/Data/mousecagemaps/' + 'box_' + str(box_nr)

	f = open(openstr,'w+b')
	f.write(str(request.POST['mouseID']))
	f.close()
	return HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))
	

#________________________________________________________________________________________________________

def set_mouse_task(request,box_nr):

	if request.method == 'GET':
		ssh_dest =   r'pi@192.168.' + str(100 + int(box_nr))
		p = subprocess.Popen(["ssh", "%s" % ssh_dest, "ls /home/pi/behaviour_scripts"],
				      shell=False, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		tasks = p.stdout.readlines()

		context = {'box_nr': box_nr,'taskList':tasks}
		return render(request, 'getData/set_mouse_task.html',context)
	

	if request.method == 'POST':
		ssh_dest =   r'pi@192.168.' + str(100 + int(box_nr))
		p = subprocess.Popen(["ssh", "%s" % ssh_dest, "python /home/pi/behaviour_scripts/" + request.POST.get('task_name')],
				      shell=False, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		retrnTxt = p.stdout.readlines()
		if (retrnTxt[0]=='hello world\n'):
			openstr = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)

			f = open(openstr,'w+b')
			task_schedule = str(request.POST['task_name'])
			f.write(task_schedule)
			f.close()
			return HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))
	

def write_mouse_task(request,box_nr):

	openstr = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)

	f = open(openstr,'w+b')

	task_schedule = str(  [ request.POST['task_name'], request.POST['duration']  ] )
	f.write(task_schedule)
	f.close()
	return HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))

	
#________________________________________________________________________________________________________


def set_num_boxes(request):
	return render(request,'getData/set_num_boxes.html')


	
def write_num_boxes(request):
	f = open('/home/rastamouse/Documents/Data/numboxes','w+b')
	toWrite = 'number_of_boxes='+ str(request.POST['newNumBoxes'])
	f.write(toWrite)
	f.close()

	return HttpResponseRedirect(reverse('getData:boxes'))

#________________________________________________________________________________________________________

def get_PiData(request,box_nr):
	context = {'box_nr': box_nr}
	return render(request,'getData/store_data_form.html',context)



def write_PiData(request,box_nr):
	
	base_path = '/home/rastamouse/Documents/Data/'

	#######
	#box_nr = request.POST['box_nr']
	openstr_MouseID = '/home/rastamouse/Documents/Data/mousecagemaps/' + 'box_' + str(box_nr)
	f = open(openstr_MouseID,'r')
	mouse_ID = f.read()
	######
	openstr_Task = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)
	f = open(openstr_Task,'r')
	task_name = f.read()
	########
	
	path = base_path + mouse_ID + task_name

	data =request.POST['piData'].split(',')

	if os.path.isdir(path):
		pass
	else:
		mkdir_p(path)


	with open( path+ r'/' 'test.csv','a') as results:
		writer = csv.writer(results,dialect='excel')
		writer.writerow(data)



	return  HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))

#________________________________________________________________________________________________________
def get_box_data(request,box_nr):

	task_schedule = get_mouse_task_schedule(box_nr, True)
	
	context = {'box_nr':box_nr}
	return render(request, 'getData/get_box_data.html',context)



#________________________________________________________________________________________________________

def download_data(request):


	base_filepath = '/home/rastamouse/Documents/Data/behaviour_data/'


	if request.method == 'GET':

		mouse_dirs = os.listdir(base_filepath+'mousewise')
		context = {'mouse_dirs': mouse_dirs}

		return render(request, 'getData/choose_box.html',context)
		

	

	


	if request.method == 'POST':
		
		path = base_filepath + request.POST.get('Mouse_ID')
		zipPath = base_filepath + r'zipfiles/' + request.POST.get('Mouse_ID') + r'.zip'
		zipf = zipfile.ZipFile(zipPath, 'w')


    		for root, dirs, files in os.walk(path):
       			 for file in files:
           			zipf.write(os.path.join(root, file))


		response = HttpResponse(zipf, content_type='application/zip')
		response['Content-Disposition'] = "attachment; filename=request.POST.get('Mouse_ID')"

		

		return response

	
	#os.path.isfile('/home/rastamouse/Documents/Data/behaviour_data')




def list_mousewise(request, mouse_ID):

	base_filepath = '/home/rastamouse/Documents/Data/behaviour_data/mousewise/'
	mouseFiles = os.listdir(base_filepath + mouse_ID)
	context = {'mouseFiles': mouseFiles,'mouse_ID': mouse_ID}
	return render(request,'getData/list_mousewise.html',context)



def download_mousewise(request, mouse_ID, fileName):

	base_filepath = '/home/rastamouse/Documents/Data/behaviour_data/mousewise/'
	filepath = base_filepath + mouse_ID + r'/' + fileName

	response = HttpResponse(open(filepath))
	response['Content-Disposition'] = "attachment; filename=test.txt"

	return response
	

#________________________________________________________________________________________________________


def upload_new_task(request,box_nr,isOnline):
    # Handle file upload
	if request.method == 'POST':
        
		sentTask = request.FILES['sentFile']
		with open('/home/rastamouse/' + sentTask.name, 'wb+') as destination:
			for chunk in sentTask.chunks():
            			destination.write(chunk)

		scp_dest =   r'192.168.' + str(100 + int(box_nr))
		os.system('scp ' + '/home/rastamouse/' + sentTask.name + ' pi@' + scp_dest + ':/home/pi/behaviour_scripts/' + sentTask.name)

            	# Redirect to the document list after POST
		return HttpResponseRedirect(reverse('getData:boxes'))
	else:


    		# Render list page with the documents and the form
		return render(request,'getData/upload_new_task.html',context={'isOnline':isOnline=='1'})

#______________________________________




""" Below are Helper functions for the views """



#_______________________________________
def get_num_boxes():
	f = open('/home/rastamouse/Documents/Data/numboxes')
	return int(re.findall(r'number_of_boxes=([0-9]+)',f.read())[0])



#_________________________________________________________________________________________________________________
def parse_task_schedule(task_schedule):

	if task_schedule!='':
		a = re.findall(r'(.*)received.*',task_schedule)
		if a==[]:
			a = task_schedule
		else:
			a = a[0]
		
		aa = ast.literal_eval(a) 
		try:

			durations = ast.literal_eval(aa[1])
			tasks = ast.literal_eval(aa[0])
			duration_str = [time_parser(dur) for dur in durations]
			#tasks = ast.literal_eval(aap)

		except:
			tasks = [str(aa[0])]
			durations = [int(aa[1])]
			duration_str = [time_parser(durations[0])]
	
	return tasks, durations,duration_str


#_________________________________________________________________________________________________________________

def time_parser(duration):

	m,s = divmod(duration,60)
	h,m = divmod(m,60)
	d,h = divmod(h,24)	

	timeStr = ("%ddays %dh:%dm:%ds" %(d,h,m,s) ) 
	return timeStr


#_________________________________________________________________________________________________________________
def get_mouse_ID(box_nr):

	openstr_MouseID = '/home/rastamouse/Documents/Data/mousecagemaps/' + 'box_' + str(box_nr)
	
	try:
	
		f = open(openstr_MouseID,'r')
	
	except IOError:
		f = open(openstr_MouseID,'w+b')
		f.write('NO_MOUSE')
		f.close()

	f = open(openstr_MouseID,'r')
	mouse_ID = f.read()
	return mouse_ID



#_________________________________________________________________________________________________________________
def get_mouse_task_schedule(box_nr,piAccess=False):

	openstr_Task = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)
	
	try:
	
		f = open(openstr_Task,'r')
	
	except IOError:
		f = open(openstr_Task,'w+b')
		f.write('NO_TASK')
		f.close()

	f = open(openstr_Task,'r')
	task_schedule = f.read()

	if piAccess:
		f = open(openstr_Task,'a')
		
		time_now = datetime.datetime.now()
		f.write('received'+str(time_now))
		f.close()

	return task_schedule


def ping_boxes(numBoxes):

	pool = Pool(10)
	active_boxes = pool.map(ping_box,range(numBoxes))

	return active_boxes


	
#_________________________________________________________________________________________________________________
def ping_box(box_nr):

	base_addr = '192.168.0.' 
	box_addr = base_addr + str(100 + int(box_nr))

	cmd = ['fping','-rn 1','-t 300',box_addr]

	try:
		a = subprocess.check_output(cmd)
		is_active = re.findall(r'.*(alive).*',a)!=[]
		if is_active:
			is_active=1
	except:
		is_active = 0


	return is_active




#_________________________________________________________________________________________________________________
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


#

def get_PiTasks(request,box_nr):
	a = subprocess.Popen(['ssh','pi@192.168.0.' + 'box_nr', 'ls'],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	available_tasks = a.stdout.readlines()
