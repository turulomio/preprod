from os import getuid, path, listdir
from sys import exit
_=str

def press_a_key_to_continue():
    print("press a key to continue")


def nmcli_net_change(netname):
    pass

def replace_in_file(file, search, replace):
    pass


def insert_in_file(filename, line, text):
    pass


def append_to_file(filename, text):
    pass

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
        if file_project in ["commons"]:
            continue
        r[file_project]=[]
        for file_action in listdir(f"{rp}/{file_project}/"):
            r[file_project].append(file_action)
    return r
