from colorama import Fore,  Style
from gettext import translation
from importlib.resources import files
from os import getuid, path, listdir, remove, chdir as os_chdir, system  as os_system
from shutil import copyfile as shutil_copyfile, rmtree as shutil_rmtree
from socket import create_connection
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
    system("read -p '{0}".format(_("Press a key to continue...")))

def nmcli_net_change(netname, check_host,  check_port, description=""):
    """
        Parameters:
            - netname with Networkmanager: str
            - ip to check: str or name
            - port to check: int
            - description="" Default description. None doesn't print anything
    """
    if description is not None:
        print_before(_("Changing net to {0}").format(netname) )
    
    retry=1
    while True:
            run(f"nmcli connection up {netname}", shell=True,  capture_output=True)
            for i in range(3):
                try:
                    with create_connection((check_host, check_port), timeout=1 ):
                        if description is not None:
                            print_after_ok()
                        return
                except:
                    if retry==1:
                        print(" " * 12, end="")
                        stdout.flush()
                    s=f"[Retrying {retry}]"
                    print("\b"*len(s)+ yellow(s),  end="")
                    stdout.flush()
                    retry+=1

def replace_in_file(filename, s, r,description=""):
    if description is not None:
        print_before(_("Replacing values in {0}").format(filename))
    data=open(filename,"r").read()
    remove(filename)
    data=data.replace(s,r)
    with open(filename, "w") as f:
        f.write(data)
    
    if description is not None:
        print_after_ok()

def lines_at_the_end_of_file(filename, s, description=""):
    if description is not None:
        print_before(_("Appending text at the end of {0}").format(filename))
    with open(filename, 'a') as f:
        f.write(s)
    if description is not None:
        print_after_ok()

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
    
    p=run(command, shell=True, capture_output=True)
    
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
    from preprod.core import concurrent_log
    print_before(_("Changing to directory {0}").format(directory),show)
    concurrent_log(_("Calling command chdir to {0}").format(directory))
    os_chdir(directory)
    print_after_ok(show)

def git_clone(url):
    run_and_check(f"git clone {url}", description=f"Cloning git repository {url}")

def git_pull():
    run_and_check("git pull", description="Pulling git repository")

def insert_at_line(file_path, line_number, text, description=""):
    """
        Parameters
          - line_number is the number of lines not a zero-based index
          - text must be the content of a line without \n
    """
    if description is not None:
        print_before(_("Insert text at line {0} in {1}").format(line_number, file_path))

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Adjust line number to zero-based index
    line_number -= 1

    if line_number < 0 or line_number > len(lines):
        if description is not None:
            print_after_error()
        raise IndexError(_("Line number is out of range"))

    lines.insert(line_number, text + '\n')

    with open(file_path, 'w') as file:
        file.writelines(lines)

    if description is not None:
        print_after_ok()


def copyfile(from_,  to_):
    shutil_copyfile(from_,  to_)

def delete_line_in_file(file_path, line_number, description=""):
    if description is not None:
        print_before(_("Deleting line {0} in {1}").format(line_number, file_path))

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Adjust line number to zero-based index
    line_number -= 1

    if line_number < 0 or line_number >= len(lines):
        raise IndexError(_("Line number is out of range"))

    del lines[line_number]

    with open(file_path, 'w') as file:
        file.writelines(lines)

    if description is not None:
        print_after_ok()



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
    
    
    run_and_check(f"{python_version_name} -m venv {str_sss} .{python_version_name}", description= f"Creating virtual env at .{python_version_name}")
    return ".python3.11/bin/python3", ".python3.11/bin/pip"

def apache_initd_restart():
    run_and_check("/etc/init.d/apache2 restart", "Restarting apache server")
    

def npm_install():
    run_and_check("npm install")
    
