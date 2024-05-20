from colorama import Fore,  Style
from gettext import translation
from importlib.resources import files
from os import getuid, path, listdir, remove, chdir as os_chdir, system  as os_system
from shutil import copyfile as shutil_copyfile, rmtree as shutil_rmtree
from subprocess import run
from sys import exit, stdout

try:
    t=translation('preprod', files("preprod") / 'locale')
    _=t.gettext
except:
    _=str

def red(s):
        return Fore.RED + Style.BRIGHT + s + Style.RESET_ALL
        
def green(s):
        return Fore.GREEN + Style.BRIGHT + s + Style.RESET_ALL

def yellow(s):
        return Fore.YELLOW+ Style.BRIGHT + s + Style.RESET_ALL

def white(s):
        return Style.BRIGHT + s + Style.RESET_ALL

def press_a_key_to_continue():
    print("  * press a key to continue")


def nmcli_net_change(netname):
    pass

def replace_in_file(filename, s, r,description=""):
    if description is not None:
        print_before(_("Replacing values in {0}").format(filename))
    data=open(filename,"r").read()
    remove(filename)
    data=data.replace(s,r)
    f=open(filename, "w")
    f.write(data)
    f.close()
    if description is not None:
        print_after_ok()

def lines_at_the_end_of_file(filename, s):
    f = open(filename, 'a')
    f.write(s)
    f.close()

def run_and_check(command,  description=None,  expected_returncode=0,  expected_stdout=None, verbose=True):
    """
        Executes a comand and returns a boolean if command was executed as expected
        
        Parameters:
            - verbose. If true shows stdout and stderr
            - description. None makes not output, "" print command, else prints else
    """
    if description is not None:
        if description=="":
            description=command
        
        print (f"  - {description} ",  end="")
        stdout.flush()
    
    p=run(command, shell=True, capture_output=True);
    
    #Check if process is valid
    r=False
    if expected_stdout is not None:
        print(expected_stdout, )
        r= expected_stdout in p.stdout.decode('utf-8')
        r=True
    elif p.returncode==expected_returncode:
        r=True
    
    if r is False and verbose is True:
        print(f"Error en comando. {command}")
        print("STDOUT:")
        print(p.stdout.decode('utf-8'))
        print("STDERR:")
        print(p.stderr.decode('utf-8'))
        print(_("Exiting propred..."))
        
    if description is not None:
        if r is True:
            print (f"[{green('OK')}]")
        else:
            print (f"[{red('ERROR')}]")
    return r

def print_before(s, show=True):
    if show:
        print (f"  - {s} ",  end="")
        stdout.flush()

def print_after_ok(show=True):
    if show:
        print (f"[{green('OK')}]")

def print_after_error(show=True):
    if show:
        print (f"[{red('ERROR')}]")

def system(command):
    os_system(command)

def rmtree(directory, show=True):
    print_before(_("Deleting directory {0}").format(directory),show)
    shutil_rmtree(directory, ignore_errors=True)
    print_after_ok(show)
    
def chdir(directory, show=True):
    print_before(_("Changing to directory {0}").format(directory),show)
    os_chdir(directory)
    print_after_ok(show)

def git_clone(url):
    run_and_check(f"git clone {url}", description=f"Cloning git repository {url}")

def git_pull():
    run_and_check("git pull", description="Pulling git repository")

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

def create_python_virtual_env(python_version_name="python3.11", system_site_packages=False):
    """
        Will create a python virtual env in .python_version_name with python_version_name executable
        Parameters:
           - python_version_name: str: python3.11
    """
    str_sss=""
    if system_site_packages:
        str_sss="--system-site-packages"
    
    
    run_and_check(f"{python_version_name} -m venv {str_sss} .{python_version_name}", description= f"Creating virtual env at .python3.11")
    return ".python3.11/bin/python3", ".python3.11/bin/pip"

def apache_initd_restart():
    run_and_check("/etc/init.d/apache2 restart", "Restarting apache server")
    

def npm_install():
    run_and_check("npm install")
    