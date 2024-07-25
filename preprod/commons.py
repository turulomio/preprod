from colorama import Fore,  Style
from getpass import getuser as getpass_getuser
from gettext import translation
from importlib.resources import files
from os import getuid, path, listdir, remove, chdir as os_chdir, system  as os_system, makedirs as os_makedirs, getcwd
from shutil import copyfile as shutil_copyfile, rmtree as shutil_rmtree
from socket import create_connection
from subprocess import run, Popen, PIPE
from sys import exit, stdout

"""
    Each command should have these parameters
    - description: (None: Doesn't show anything, "": Show default description, "something": "Shows something as description")

"""


try:
    t=translation('preprod', files("preprod") / 'locale')
    _=t.gettext
except:
    _=str



def red(s):
    """
        Prints string in red and bright color
    """
    return Fore.RED + Style.BRIGHT + s + Style.RESET_ALL
        
def green(s):
    """
        Prints string in green and bright color
    """
    return Fore.GREEN + Style.BRIGHT + s + Style.RESET_ALL

def yellow(s):
    """
        Prints string in yellow and bright color
    """
    return Fore.YELLOW+ Style.BRIGHT + s + Style.RESET_ALL

def white(s):
    """
        Prints string in white and bright color
    """
    return Style.BRIGHT + s + Style.RESET_ALL

def press_a_key_to_continue():
    """
        Waits until user press a key
    """
    from preprod.core import concurrent_log
    concurrent_log("Before press a key to continue...")
    system("read -p '{0}'".format(_("Press a key to continue...")))
    concurrent_log("After press a key to continue...")

def makedirs(dirname, description=""):
    """
        Create directories to last child. If it's already created ignores error
    """
    from preprod.core import concurrent_log
    log=_("Created {0} directory").format(dirname)
    description=log if description=="" else description
    print_before(description, description is not None)
    os_makedirs(dirname,  exist_ok=True)
    concurrent_log(log)
    print_after_ok(description is not None)
    


def nmcli_net_change(netname, check_host,  check_port, socket_timeout=2, number_of_sockets=5, description=""):
    """
        Uses nmcli to change a net and waits until can connect to check_host:check_port

        Parameters:
            - netname with Networkmanager: str
            - ip to check: str or name
            - port to check: int
            - description="" Default description. None doesn't print anything
    """
    if description is not None:
        print_before(_("Changing net to {0}").format(netname) )
    
    retry=1
    from preprod.core import concurrent_log
    concurrent_log(f"Before changing net to {netname}")
    while True:
        p=run(f"nmcli connection up {netname}", shell=True,  capture_output=True)
        concurrent_log(p.returncode)
        for i in range(number_of_sockets):
            try:
                with create_connection((check_host, check_port), timeout=socket_timeout):
                    if description is not None:
                        print_after_ok()
                    concurrent_log(f"After changing net to {netname}")
                    return
            except:
                if retry==1:
                    print(" " * 12, end="")
                    stdout.flush()
                s=f"[Retrying {retry}] " +"."*i
                print("\b"*len(s)+ yellow(s),  end="")
                stdout.flush()
                concurrent_log(f"Connection exception retry {retry}. Socket {i+1}/{number_of_sockets}.")
                retry+=1


def replace_in_file(filename, s, r,description=""):
    """
        Replaces a string for other in the whole file
    """
    description=_("Replacing values in {0}").format(filename) if description=="" else description
    print_before(description, description is not None)
    data=open(filename,"r").read()
    remove(filename)
    data=data.replace(s,r)
    with open(filename, "w") as f:
        f.write(data)
    print_after_ok(description is not None)
    from preprod.core import concurrent_log
    concurrent_log(f"Replaced in file '{filename}', '{s}' by '{r}'")

def lines_at_the_end_of_file(filename, s, description=""):
    """
        Appends a string (for lines append \n) to the end of the file
    """
    print_before(_("Appending text at the end of {0}").format(filename), description is not None)
    with open(filename, 'a') as f:
        f.write(s)
    print_after_ok(description is not None)
    from preprod.core import concurrent_log
    concurrent_log(f"Added at the of file '{filename}'", s)
    
    

def system(command, user=None, description=""):
    """
        Runs a command with system
    """
    
    if user is not None:
        command=f"""su - {user} -c "cd '{getcwd()}' && {command}" """
        log=_("Running '{0}' as user '{1}' with system command").format(command, user)
        description=log if description=="" else description
    else:
        log=_("Running '{0}' with system command").format(command) 
        description=log if description=="" else description
    print_before(description, description is not None)
    from preprod.core import concurrent_log
    concurrent_log(log)
    os_system(command)

def run_and_check(command, user=None, userpassword=None,    description="",  expected_returncode=0,  expected_stdout=None):
    """
        Executes a command as another user and checks if it was executed as expected.

        Args:
        - command (str): The command to execute.
        - username (str): The username of the user under whom to execute the command.
        - description (str, optional): Description of the command (for logging purposes).
        - expected_returncode (int, optional): Expected return code of the command.
        - expected_stdout (str, optional): Expected output in stdout.

        Returns:
        - bool: True if the command was executed as expected, False otherwise.
    """
    
    if user is not None:
        command=f"su - {user} -c '{command}'"
        description=_("Running '{0}' as user '{1}'").format(command, user) if description=="" else description
    else:
        description=_("Running '{0}'").format(command) if description=="" else description
    
    print_before(description, description is not None)
    
    if userpassword is None:
        p=run(command, shell=True, capture_output=True)
    else:
        p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=getcwd())

        # Pass password to su using stdin.write
        p.stdin.write(userpassword.encode('utf-8') + b'\n')
        p.stdin.flush()

        # Wait for the command to complete and get stdout and stderr
        stdout, stderr = p.communicate()

    
    #Check if process is valid
    r=False
    if expected_stdout is not None:
        print(expected_stdout, )
        r= expected_stdout in p.stdout.decode('utf-8')
        r=True
    elif p.returncode==expected_returncode:
        r=True
    
    if r is True:
        print_after_ok(description is not None)
    else:
        print_after_error(description is not None)
            
    from preprod.core import concurrent_log
    if userpassword is None:
        stdout_=p.stdout.decode('utf-8')
        stderr_=p.stderr.decode('utf-8')
    else:
        stdout_=stdout.decode('utf-8')
        stderr_=stderr.decode('utf-8')
    if  user is None:
        concurrent_log(f"run_and_check('{command}')",  stdout_, stderr_)
    else:
        concurrent_log(f"run_and_check('{command}')",  stdout_, stderr_)
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

def rm(filename, description=""):
    """
        Removes a file
    """
    
    description=_("Removing file '{0}'").format(filename) if description=="" else description
    run_and_check(f"rm '{filename}'", description=description)

def rmtree(directory, show=True):
    """
        Deletes a directory recursively. It directory doesn't exist ignores error

        Be careful
    """
    print_before(_("Deleting directory {0}").format(directory),show)
    shutil_rmtree(directory, ignore_errors=True)
    print_after_ok(show)
    from preprod.core import concurrent_log
    concurrent_log(f"rmtree('{directory}')")
    
def chdir(directory, show=True):
    """
        Changes to a directory
    """
    from preprod.core import concurrent_log
    print_before(_("Changing to directory {0}").format(directory),show)
    concurrent_log(f"chdir('{directory}')")
    os_chdir(directory)
    print_after_ok(show)
    
    
def getuser():
    """
        Returns a string with current user
    """
    return getpass_getuser()
    
def file_contains_string(file_path, search_string):
    """
    Check if the specified file contains the given string.
    
    Args:
    file_path (str): The path to the file.
    search_string (str): The string to search for in the file.

    Returns:
    bool: True if the file contains the string, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read through the file
            for line in file:
                if search_string in line:
                    return True
        return False
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def git_clone(url,  output_directory="", branch=None, description=""):
    """
        Clones a git project using its url. If you need a different output directory you can set in params
    """
    branch_string="" if branch is None else f"--branch {branch}"
    if branch is None and output_directory=="":
        description=_("Cloning git repository '{0}'").format(url) if description=="" else description
    elif branch is None and output_directory!="":
        description=_("Cloning git repository '{0}' into '{1}' directory").format(url, output_directory) if description=="" else description
    elif branch is not None and output_directory=="":
        description=_("Cloning branch '{0}' of git repository '{1}'").format(branch,  url) if description=="" else description
    else:
        description=_("Cloning branch '{0}' of git repository '{1}' into '{2}' directory").format(branch,  url,  output_directory) if description=="" else description
    run_and_check(f"git clone {branch_string} {url} {output_directory}", description=description)

def git_pull(description=""):    
    """
        Updates git repository using git pull command
    """
    description=_("Pulling git repository") if description=="" else description
    run_and_check("git pull", description=description)

def insert_at_line(file_path, line_number, text, description=""):
    """
        Inserts a line using the number of the line

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
        
    from preprod.core import concurrent_log
    concurrent_log(f"insert_at_line('{file_path}', {line_number})", text)


def copyfile(from_,  to_):
    """
        Copies a file
    """
    shutil_copyfile(from_,  to_)
    from preprod.core import concurrent_log
    concurrent_log(f"copyfile('{from_}', '{to_}')")

def delete_line_in_file(file_path, line_number, description=""):

    """
        Deletes a line in a file
    """
    if description is not None:
        print_before(_("Deleting line {0} in {1}").format(line_number, file_path))

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Adjust line number to zero-based index
    line_number -= 1

    if line_number < 0 or line_number >= len(lines):
        raise IndexError(_("Line number is out of range"))
        
    to_delete=lines[line_number]

    del lines[line_number]

    with open(file_path, 'w') as file:
        file.writelines(lines)

    if description is not None:
        print_after_ok()
    from preprod.core import concurrent_log
    concurrent_log(f"delete_line_in_file('{file_path}', {line_number})", None,  to_delete)



def is_root():
    """
        Returns if current user is root
    """
    return getuid() == 0
    
    
def kill_from_ps_aux(pattern, description=""):
    """
        Searchs a case sensitive pattern in ps aux command. It will kill all process with this pattern throug its pid using kill command
    """
    description=_("Killing all process that contain '{0}' in ps aux.").format(pattern) if description=="" else description
    print_before(description, description is not None)

    r=run("ps aux",  shell=True,  capture_output=True)
    s=r.stdout.decode("UTF-8")
    
    detected=0
    killed=0
    kill_output=""
    for line in s.split("\n"):
        if pattern in line:
            detected+=1
            pid=line[9:].split(" ")[0]
            k=run(f"kill -9 {pid}", shell=True,  capture_output=True)
            kill_output+=k.stdout.decode("UTF-8")+"\n"
            if k.returncode==0:
                killed+=1


    print( _("Found {0}. Killed {1}").format(detected, killed) +" ",  end="")
    stdout.flush()
    if detected==killed and detected>0:
        print_after_ok(description is not None)
    else:
        print_after_error(description is not None)

    from preprod.core import concurrent_log
    concurrent_log(description, kill_output)
    
def repository_path():
    """
        Returns repository path
    """
    if is_root():
        return "/etc/preprod/"
    else:
        return f"{path.expanduser('~')}/.preprod/"
        
def check_repository_path(verbose=False):
    """
        Gets with a boolean if repository path exists
    """
    if path.exists(repository_path()):
        return True
    else:
        if verbose is True:
            print (_("You must create repository path"))
            exit(5)
        return False
        
def dictionary_project_actions():
    """
        Returns a dictioanry with all projects and actions
    """
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
    str_sss="--system-site-packages" if system_site_packages else ""
    run_and_check(f"{python_version_name} -m venv {str_sss} .{python_version_name}", description= f"Creating virtual env at .{python_version_name}")
    return path.abspath(f".{python_version_name}/bin/python3"), path.abspath(f".{python_version_name}/bin/pip")

def apache_initd_restart(description=""):
    """
        Starts apache using init.d script
    """
    description=_("Restarting apache server") if description=="" else description
    run_and_check("/etc/init.d/apache2 restart", description=description)
    
def chown_recursive(path,  user="root",  group="root", description=""):
    description=_("Changing '{0}' to owner {1}:{2}").format(path, user,  group) if description=="" else description
    run_and_check(f"find {path} -type f -exec chown -R {user}:{group} {{}} +", description=description)

def chmod_recursive(path,  directory_permissions="755",  file_permissions="644",  description=""):
    description=_("Changing directories permissions to {0} and files to {1}").format(directory_permissions, file_permissions) if description=="" else description
    run_and_check(f"find {path} -type d -exec chmod -R {directory_permissions} {{}} +", description=None)
    run_and_check(f"find {path} -type f -exec chmod -R {file_permissions} {{}} +", description=description)


def create_a_file(filename, content, description=""):
    """
        Creates a new file or replaces it with content parameter
    """
    description=_(f"Creating file '{filename}'") if description=="" else description
    print_before(description, description is not None)
    with open(filename, "w") as f:
        f.write(content)
    print_after_ok(description is not None)
    from preprod.core import concurrent_log
    concurrent_log(description, content)

def npm_install(description=""):
    run_and_check("npm install", description=description)
    
def rsync(from_,  to_,  delete_after=False, description=""):
    str_delete_after="--delete-after" if delete_after else ""
    run_and_check(f"rsync -avzPH {from_} {to_} {str_delete_after}", description=description)
    
def poetry_install(description=""):
    run_and_check("poetry install", description=description)
    
def poetry_env_info():
    """
        Return the path to the python executable and pip executable inside current dir poetry virtualenv
    """
    p=run("poetry env info -e", shell=True, capture_output=True)
    python_=p.stdout.decode('utf-8')[:-1]
    pip_=python_.replace("bin/python",  "bin/pip")
    return python_,  pip_
