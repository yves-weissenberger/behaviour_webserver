import os
import sys

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
    os.mkdir(os.path.join(path,'socket_server'))
    os.mkdir(os.path.join(path,'socket_server','box_video_info'))


    with open(os.path.join(path,'numboxes.txt'),'w') as f:
        f.write("number_of_boxes=0")

    with open(os.path.join(proj_dir,'mysite','settings.py'),'r') as f:
        # read the file into a list of lines
        lines = f.readlines()


    with open(os.path.join(proj_dir,'mysite','settings.py'),'w') as f:
        # now edit the last line of the list of lines
        new_last_line = 'MEDIA_ROOT=' + '"'  + path  + '"'
        lines[-1] = new_last_line

        # now write the modified list back out to the file
        f.writelines(lines)




