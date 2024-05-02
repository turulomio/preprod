from os import getuid, path, listdir, remove, chdir as os_chdir, system  as os_system
from shutil import copyfile as shutil_copyfile
from subprocess import run
from sys import exit
_=str

def press_a_key_to_continue():
    print("press a key to continue")


def nmcli_net_change(netname):
    pass

def replace_in_file(filename, s, r):
    data=open(filename,"r").read()
    remove(filename)
    data=data.replace(s,r)
    f=open(filename, "w")
    f.write(data)
    f.close()

def lines_at_the_end_of_file(filename, s):
    f = open(filename, 'a')
    f.write(s)
    f.close()

def run_check(command):
    p=run(command, shell=True, capture_output=True);
    if p.returncode!=0:
        print(f"Error en comando. {command}")
        print("STDOUT:")
        print(p.stdout.decode('utf-8'))
        print("STDERR:")
        print(p.stderr.decode('utf-8'))
        print(_("Exiting propred..."))
        exit(2)

def system(command):
    os_system(command)

def chdir(directory):
    os_chdir(directory)
    
def git_pull():
    run_check("git pull")

def insert_in_file(filename, line, text):
    pass


def append_to_file(filename, text):
    pass

def copyfile(from_,  to_):
    shutil_copyfile(from_,  to_)

def delete_line_in_file(filename, line):
    pass

def is_root():
    """
        Returns if current user is root
    """
    return getuid() == 0
    
def repository_path():
    """
        Returns repository path
    """
    if is_root():
        return "/etc/preprod/"
    else:
        return f"{path.expanduser('~')}/.preprod/"
        
def check_repository_path(verbose=False):
    if path.exists(repository_path()):
        return True
    else:
        if verbose is True:
            print (_("You must create repository path"))
            exit(5)
        return False
        
def dictionary_project_actions():
    r={}
    rp=repository_path()

    print(_("Reading repository from {0}").format(rp))

    for file_project in listdir(rp):
        if file_project in ["repository_commons.py", "__pycache__"]:
            continue
        r[file_project]=[]
        for file_action in listdir(f"{rp}{file_project}/"):
            r[file_project].append(file_action)
    return r
