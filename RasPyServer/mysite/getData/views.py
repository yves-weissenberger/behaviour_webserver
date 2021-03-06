import sys

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

if sys.version_info[0] < 3:
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


from django.contrib.auth.decorators import login_required
#________________
from django.utils.timezone import utc
import datetime
from django.utils.safestring import mark_safe
import json
from django.conf.urls.static import static
from django.conf import settings


#________________
import os, errno
import csv
import os
import re
import time
import ast
import subprocess
from multiprocessing.dummy import Pool
import zipfile
import json
import subprocess
import pathlib
from django.http import JsonResponse

#________________________________________________________________________________________________________


with open(os.path.join(os.path.split(os.path.split(__file__)[0])[0],"ROOT_dir.txt"),'r') as f:
    ROOT_path = re.findall(r"ROOT_dir=(.*)",f.readline())[0]

#ROOT_path = os.path.split(os.path.split(__file__)[0])[0]
#ROOT_path = '/home/rastamouse/Documents/Data/'


def _get_task_fName(box_nr):



    openstr_MouseID = os.path.join(ROOT_path,'mousecagemaps','box_'+str(box_nr))
    with open(openstr_MouseID,'r') as f:
        mouse_ID = f.read()
    ######
    openstr_Task = os.path.join(ROOT_path,'cage_tasks','box_'+str(box_nr))

    #openstr_Task = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)
    try:
        with open(openstr_Task,'r') as f:
            task_schedule = f.read()
        ########
        #task_schedule = get_mouse_task_schedule(box_nr)
        task = re.findall(r'(.*).py_',task_schedule)[0]
        startT = re.findall(r'_received(.*)',task_schedule)[0]
    except IndexError:
        print("Warning no task set recording in generic location")
        task = "random"
        startT = str(datetime.datetime.now().replace(microsecond=0)).replace(" ",'-')


    fName = "_".join([mouse_ID,task,startT.replace(":",'-').replace(" ",'-')])

    return fName, (mouse_ID,task,startT)






def get_plot_data(request,box_nr):
    root_dir = os.path.split(settings.MEDIA_ROOT)[0]

    print ("NOOOOOT BAD")
    fName, temp_ = _get_task_fName(box_nr)
    dir_pth = os.path.join(root_dir,'behaviour_data','mousewise',temp_[0])
    fPath = os.path.join(dir_pth,fName+".csv")
    varss, evs, var_elem_sets, var_elem_setsFullN, countL = proc_dat(fPath)
    timedict= {'vars': varss,
               'var_elem_flat': [item for sublist in var_elem_setsFullN for item in sublist],
               'count_elem_flat': countL,
               'counts':1}
    return JsonResponse(timedict)




def proc_dat(pth):
    
    with open(pth,'r') as f:
        lines = f.readlines()

    varss = re.findall(r"([A-z]+)List:",lines[0])


    evs = []
    for ind,v in enumerate(varss):
        temp_var = [[],[]]
        for i in range(len(lines)):
            temp  = re.findall(v+"List:(.*?)[,|\n]",lines[i])[0].split("-")
            #ts = [re.findall(r"([0-9]*\.[0-9]{1,3})",i)[0] for i in temp if i!='']
            temp = [i for i in temp if i!='']
            times = []
            ts = [i.split("_")[0] for i in temp]
            evTs = [i.split("_")[1] for i in temp]

            temp_var[0].extend([float(i) for i in ts])
            temp_var[1].extend(evTs)
        if len(temp_var[0])!=0:
            evs.append(temp_var)

    var_elem_sets = []
    var_elem_setsFullN = []

    kk = 0
    for i,j in evs:
        if len(i)!=0:
            var_elem_sets.append(list(set(j)))
            var_elem_setsFullN.append([varss[kk]+i for i in list(set(j))])

        kk += 1

    countL = []
    for i,j in zip([i[1] for i in evs],var_elem_sets):
        for k in j:
            countL.append(i.count(k))
    return varss, evs, var_elem_sets, var_elem_setsFullN, countL






def start_video_server(request,box_nr):

    """ Opens a python process running a socket server if request is to start this. Otherwise kills it
        Also saves the pid of the python process to text file for later working with"""
    root_dir = os.path.split(settings.MEDIA_ROOT)[0]

    fName, temp = _get_task_fName(box_nr)

    mouse_ID,task,startT = temp
    fold_path0 = os.path.join(ROOT_path,"socket-server","data",mouse_ID)

    if os.path.isdir(fold_path0):
        pass
    else:
        mkdir_p(fold_path0)

    fold_path1 = os.path.join(ROOT_path,"socket-server","data",mouse_ID,fName)

    if os.path.isdir(fold_path1):
        pass
    else:
        mkdir_p(fold_path1)





    # This opens a server 
    script_pth = os.path.join(root_dir,'socket-server',"video_server.py")
    pth_pids = os.path.join(ROOT_path,"socket-server","box_video_info")
    with open(os.path.join(pth_pids,'box_'+str(box_nr)),'r') as f:
        ppid = f.readline()






    if re.findall(r'[0-9]+',ppid):
        print ('aleady running')
        #os.kill(ppid)

    sp = subprocess.Popen(['python', script_pth,str(box_nr),fold_path1],shell=0)
    with open(os.path.join(pth_pids,'box_'+str(box_nr)),'w') as f:
        f.write(str(sp.pid))
        f.write("\n")
        f.write(fold_path1)

  



    sp_remote = subprocess.Popen(["ssh","pi@192.168.0."+str(100+int(box_nr)),"python ~/socket_video/video_provider.py"],
        shell=False, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    remote_pid = sp_remote.stdout.readlines()
    #print (os.path.split(os.path.split(settings.MEDIA_ROOT)[0]))
    return HttpResponse("Text")

def stop_video_server(request,box_nr):
    pth_pids = os.path.join(ROOT_path,"socket-server","box_video_info")
    fullP = os.path.join(pth_pids,'box_'+str(box_nr))

    with open(fullP,'r') as f:
        temp = f.readline()
    temp2 = str(re.findall(r'[0-9]+',temp)[0])
    sp_remote = os.system("kill " + "$(cat " + str(fullP)+")")

    #sp_remote = subprocess.check_output(["kill", str(temp2)])
    #sp_remote = subprocess.check_output(["kill " + "$(cat " + fullP+")"])
    sp_remote = os.system("kill " + "$(cat " + fullP+")")

    with open(fullP,'w') as f:
        temp = f.write("None")
    return HttpResponse("Text")


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
    numBoxes = get_num_boxes()


    box_connected = ping_box(box_nr)
    #box_connected = is_online=='True'
    mouse_ID = get_mouse_ID(box_nr)

    task = "None"
    time_elapsed = ""
    try:
        task_schedule = get_mouse_task_schedule(box_nr)
        task = re.findall(r'(.*).py_',task_schedule)[0]
        startT = re.findall(r'_received(.*)',task_schedule)[0]


        time_received = datetime.datetime.strptime(startT, '%Y-%m-%d %H:%M:%S')
        time_elapsed_tdelta = datetime.datetime.now() - time_received
        time_elapsed = time_parser(time_elapsed_tdelta.total_seconds() )
        print (time_elapsed)
    except IndexError:
        pass
            




    context = {'box_nr': box_nr,'mouse_ID':mouse_ID,
           'task_name': str(task),
           'time_elapsed': str(time_elapsed),
           'isOnline':box_connected,
           'boxs':range(numBoxes),
           'dataStr': ''}


    return render(request,'getData/box_info.html',context)



#________________________________________________________________________________________________________
def set_mouse_ID(request,box_nr):
    
    context = {'box_nr': box_nr}
    return render(request, 'getData/set_mouse_ID.html',context)

    
def write_mouse_ID(request,box_nr):

    pth = os.path.join(ROOT_path,'mousecagemaps','box_' + str(box_nr))
    print (request.POST.keys())
    #openstr = '/home/rastamouse/Documents/Data/mousecagemaps/' + 'box_' + str(box_nr)
    with open(pth,'w') as f:
        f.write(str(request.POST['mouse_ID']))
    return HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))
    

#________________________________________________________________________________________________________

def set_mouse_task(request,box_nr):

    if request.method == 'GET':
        ssh_dest =   r'pi@192.168.' + str(100 + int(box_nr))
        p = subprocess.Popen(["ssh", "%s" % ssh_dest, "ls /home/pi/behaviour_scripts"],
                      shell=False, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        tasks = p.stdout.readlines()
        tasks = [i.decode("utf-8").replace('\n','').replace('\\n','') for i in tasks]
        print (tasks)
        print(type(tasks))

        context = {'box_nr': box_nr,'taskList':tasks}
        return render(request, 'getData/set_mouse_task.html',context)
    

    if request.method == 'POST':
        ssh_dest =   r'pi@192.168.' + str(100 + int(box_nr))
        p = subprocess.Popen(["ssh", "%s" % ssh_dest, "python /home/pi/behaviour_scripts/" + request.POST.get('task_name')],
                      shell=False, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        retrnTxt = p.stdout.readlines()
        print(retrnTxt)
        if "hello" in retrnTxt[0].decode("utf-8"):
            pth = os.path.join(ROOT_path,'cage_tasks','box_'+str(box_nr))
            #openstr = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)
            with open(pth,'w') as f:
                task_schedule = str(request.POST['task_name'])
                f.write(task_schedule+"_received"+str(datetime.datetime.now().replace(microsecond=0)))
                f.close()
            return HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))
    

def write_mouse_task(request,box_nr):
    pth = os.path.join(ROOT_path,'mousecagemaps','box_' + str(box_nr))
    #openstr = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)

    f = open(pth,'w+b')

    task_schedule = str(  [ request.POST['task_name'], request.POST['duration']  ] )
    f.write(task_schedule)
    f.close()
    return HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))

    
#________________________________________________________________________________________________________


def set_num_boxes(request):
    return render(request,'getData/set_num_boxes.html')


    
def write_num_boxes(request):
    pth = os.path.join(ROOT_path,'numboxes.txt')
    f = open(pth,'w')
    new_N_boxes = request.POST['newNumBoxes']
    toWrite = 'number_of_boxes='+ str(new_N_boxes)
    f.write(toWrite)
    f.close()
    pth_mcm = os.path.join(ROOT_path,'mousecagemaps')
    pth_cgT = os.path.join(ROOT_path,'cage_tasks')
    pth_media = os.path.join(ROOT_path,'media')
    pth_pids = os.path.join(ROOT_path,"socket-server","box_video_info")
    nSet_cages = len(os.listdir(pth_mcm))
    for i in range(0,int(new_N_boxes)):

        print("number going now is")
        newF = os.path.join(pth_mcm,'box_'+str(i))
        with open(newF, 'w') as fi:
            fi.write("None")

        newF2 = os.path.join(pth_cgT,'box_'+str(i))
        with open(newF2, 'w') as fj:
            fj.write("None")

        newF3 = os.path.join(pth_pids,'box_'+str(i))
        #print (newF3)
        with open(newF3,'w') as fk:
            fk.write("None")

        newD1 = os.path.join(pth_media,'box_'+str(i))
        if not os.path.isdir(newD1):
            os.mkdir(newD1)
        #with open(newF2, 'w') as fj:
        #    fj.write("None")





    return HttpResponseRedirect(reverse('getData:boxes'))

#________________________________________________________________________________________________________


def get_pi_ims(request,box_nr):
    context = {'box_nr': box_nr}
    return render(request,'getData/store_images_form.html',context)

def write_pi_ims(request,box_nr):

    base_path = ROOT_path

    data = request.FILES
    #print(data.keys())
    #path = "/Users/Yves/Desktop/"
    #if not os.path.isdir(path):
    #    mkdir_p(path)
    #else:
    #    pass    
    save_pth = '/home/rastamouse/Documents/Code/RasPyServer/mysite/getData/static/getData/ims/'
    #print (len(list(data.keys())))
    if len(data.keys())==1:

        with open(save_pth+ str(len(os.listdir(save_pth))) + '.jpg','wb') as f:
            for chunk in data[list(data.keys())[0]]:
                f.write(chunk)
            #f.write(data['im.jpeg'])

    else:
        for k in list(data.keys()):

            with open(save_pth + k + '.jpg','wb') as f:
                for chunk in data[k]:
                    f.write(chunk)
        





    return  HttpResponseRedirect(reverse('getData:box_info',args=(box_nr,)))


#________________________________________________________________________________________________________


def get_PiData(request,box_nr):
    context = {'box_nr': box_nr}
    return render(request,'getData/store_data_form.html',context)


def get_f_path(box_nr):
    return None

def write_PiData(request,box_nr):
    
    base_path = ROOT_path

    #######
    #box_nr = request.POST['box_nr']
    openstr_MouseID = os.path.join(ROOT_path,'mousecagemaps','box_'+str(box_nr))
    #openstr_MouseID = '/home/rastamouse/Documents/Data/mousecagemaps/' + 'box_' + str(box_nr)
    f = open(openstr_MouseID,'r')
    mouse_ID = f.read()
    ######
    openstr_Task = os.path.join(ROOT_path,'cage_tasks','box_'+str(box_nr))

    #openstr_Task = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)
    f = open(openstr_Task,'r')
    task_name = f.read()
    ########
    task_schedule = get_mouse_task_schedule(box_nr)
    task = re.findall(r'(.*).py_',task_schedule)[0]
    startT = re.findall(r'_received(.*)',task_schedule)[0]


    fold_path = os.path.join(ROOT_path,"behaviour_data","mousewise",mouse_ID)
    #path = base_path + mouse_ID + task_name
    print("CCCLOC")
    print (fold_path)
    if os.path.isdir(fold_path):
        pass
    else:
        mkdir_p(fold_path)


    data =request.POST['piData'].split(',')

    filePath = "_".join([mouse_ID,task,startT.replace(":",'-').replace(" ",'-')]) + ".csv"
    dataPath = os.path.join(fold_path,filePath)
    with open( dataPath,'a') as results:
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

    base_filepath = os.path.join(ROOT_path,behaviour_data)
    #base_filepath = '/home/rastamouse/Documents/Data/behaviour_data/'



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

    base_filepath = os.path.join(ROOT_path,'behaviour_data','mousewise')
    #base_filepath = '/home/rastamouse/Documents/Data/behaviour_data/mousewise/'
    mouseFiles = os.listdir(base_filepath + mouse_ID)
    context = {'mouseFiles': mouseFiles,'mouse_ID': mouse_ID}
    return render(request,'getData/list_mousewise.html',context)



def download_mousewise(request, mouse_ID, fileName):
    base_filepath = os.path.join(ROOT_path,'behaviour_data','mousewise')
    #base_filepath = '/home/rastamouse/Documents/Data/behaviour_data/mousewise/'
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
    pth = os.path.join(ROOT_path,"numboxes.txt")
    f = open(pth)
    #print "HEEEELOOO", f.read()
    #nb = int(re.findall(r'number_of_boxes=([0-9]+)',f.read())[0])
    #print "))))))", nb
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
    openstr_MouseID = os.path.join(ROOT_path,'mousecagemaps', 'box_' + str(box_nr))

    #openstr_MouseID = '/home/rastamouse/Documents/Data/mousecagemaps/' + 'box_' + str(box_nr)
    
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
    openstr_Task = os.path.join(ROOT_path,'cage_tasks','box_'+str(box_nr))

    #openstr_Task = '/home/rastamouse/Documents/Data/cage_tasks/' + 'box_' + str(box_nr)
    
    try:
    
        f = open(openstr_Task,'r')
    
    except IOError:
        f = open(openstr_Task,'w')
        f.write('NO_TASK')
        f.close()

    f = open(openstr_Task,'r')
    task_schedule = f.read()

    if piAccess:
        f = open(openstr_Task,'a')
        
        time_now = datetime.datetime.now().replace(microsecond=0)
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

    cmd = ['fping','-t 300','-r 1',box_addr]
    #a = subprocess.check_output(cmd)
    #print(a)
    #print ("HELLO")
    try:
        a = subprocess.check_output(cmd)
        print(a)
        if 'alive' in str(a):
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
