import os
import sys
from shutil import copyfile

if __name__=='__main__':

    proj_dir = os.path.split(os.path.realpath(__file__))[0]
    print (proj_dir)

    path = str(input("Specify path to target directory:"))
    print (path)
    with open(os.path.join(proj_dir,"ROOT_dir.txt"),'w') as f:
        f.write("ROOT_dir="+path)

    if not os.path.isdir(path):
        os.mkdir(path)

    if not os.path.isdir(os.path.join(path,'behaviour_data')):
    	os.mkdir(os.path.join(path,'behaviour_data'))

    os.mkdir(os.path.join(path,'behaviour_data','mousewise'))
    os.mkdir(os.path.join(path,'cage_tasks'))
    os.mkdir(os.path.join(path,'mousecagemaps'))
    os.mkdir(os.path.join(path,'media'))
    os.mkdir(os.path.join(path,'socket-server'))
    vid_server_py = os.path.join(os.path.split(proj_dir)[0],'aux','socket-server',"video_server.py")
    #vid_server_py = os.path.join(os.path.split(proj_dir)[0],'aux','socket_server',"vid_server.py")
    copyfile(vid_server_py, os.path.join(path,'socket-server','video_server.py'))

    os.mkdir(os.path.join(path,'socket-server','box_video_info'))


    with open(os.path.join(path,'numboxes.txt'),'w') as f:
        f.write("number_of_boxes=0")

    with open(os.path.join(proj_dir,'mysite','settings.py'),'r') as f:
        # read the file into a list of lines
        lines = f.readlines()


    with open(os.path.join(proj_dir,'mysite','settings.py'),'w') as f:
        # now edit the last line of the list of lines

        lines[-1] = "MEDIA_URL = '/media/'"

        new_media_root = 'MEDIA_ROOT=' + '"'  + path  + '"\n'
        lines[-2] = new_media_root


        # now write the modified list back out to the file
        f.writelines(lines)




