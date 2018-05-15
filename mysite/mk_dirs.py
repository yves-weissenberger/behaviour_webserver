import os
import sys
if __name__=='__main__':
    path = raw_input("Specify path to target directory:")
    
    proj_dir = os.path.split(os.path.realpath(__file__))[0]

    with open(os.path.join(proj_dir,"ROOT_dir.txt"),'wb') as f:
        f.write("ROOT_dir="+path)

    if not os.path.isdir(path):
        os.mkdir(path)

    if not os.path.isdir(os.path.join(path,'behaviour_data')):
    	os.mkdir(os.path.join(path,'behaviour_data'))

    os.mkdir(os.path.join(path,'behaviour_data','mousewise'))
    os.mkdir(os.path.join(path,'cage_tasks'))
    os.mkdir(os.path.join(path,'mousecagemaps'))

    with open(os.path.join(path,'numboxes.txt'),'wb') as f:
        f.write("number_of_boxes=0")



