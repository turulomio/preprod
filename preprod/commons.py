from colorama import Fore,  Style
from getpass import getuser as getpass_getuser
from gettext import translation
from importlib.resources import files
from os import getuid, path, listdir, remove, chdir as os_chdir, system  as os_system, makedirs as os_makedirs, getcwd
from shutil import copyfile as shutil_copyfile, rmtree as shutil_rmtree
from socket import create_connection
from subprocess import run, Popen, PIPE
from time import sleep as time_sleep
from sys import exit, stdout
from .version import __version__, __versiondate__


"""
This module provides a collection of common utility functions used across the preprod project.
It includes functions for colored console output, file system operations, process execution,
network checks, Git operations, and repository management, among others.
"""


"""
    Each command should have these parameters
    - description: (None: Doesn't show anything, "": Show default description, "something": "Shows something as description")

"""


try:
    t=translation('preprod', files("preprod") / 'locale')
    _=t.gettext
except:
    _=str

def epilog():
    """
    Generates the epilog string for the argument parser, including version information.

    Returns:
        str: A formatted string containing the developer's name and the project's version date.
    """
    return _("Developed by Mariano Muñoz {}-{}").format(__versiondate__.year, __versiondate__.year)


def red(s):
    """
    Returns the input string formatted in bright red color for console output.

    Args:
        s (str): The string to colorize.
    Returns:
        str: The colorized string.
    """
    return Fore.RED + Style.BRIGHT + s + Style.RESET_ALL
        
def green(s):
    """
    Returns the input string formatted in bright green color for console output.

    Args:
        s (str): The string to colorize.
    Returns:
        str: The colorized string.
    """
    return Fore.GREEN + Style.BRIGHT + s + Style.RESET_ALL

def yellow(s):
    """
    Returns the input string formatted in bright yellow color for console output.

    Args:
        s (str): The string to colorize.
    Returns:
        str: The colorized string.
    """
    return Fore.YELLOW+ Style.BRIGHT + s + Style.RESET_ALL

def white(s):
    """
    Returns the input string formatted in bright white color for console output.

    Args:
        s (str): The string to colorize.
    Returns:
        str: The colorized string.
    """
    return Style.BRIGHT + s + Style.RESET_ALL

def press_a_key_to_continue():
    """
    Pauses script execution and waits for the user to press any key.
    A log entry is made before and after the wait.
    """
    from preprod.core import concurrent_log
    concurrent_log("Before press a key to continue...")
    system("read -p '{0}'".format(_("Press a key to continue...")))
    concurrent_log("After press a key to continue...")

def makedirs(dirname, description=""):
    """
    Creates a directory and any necessary parent directories.
    If the directory already exists, no error is raised.

    Args:
        dirname (str): The path of the directory to create.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
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
    Uses `nmcli` to change the network connection and then waits until a successful
    TCP connection can be established to a specified host and port.

    Args:
        netname (str): The name of the NetworkManager connection to activate.
        check_host (str): The hostname or IP address to check for connectivity.
        check_port (int): The port number to check for connectivity.
        socket_timeout (int, optional): Timeout in seconds for each socket connection attempt. Defaults to 2.
        number_of_sockets (int, optional): Number of socket connection attempts per retry cycle. Defaults to 5.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    Returns:
        None: The function exits early if `nmcli` fails with return code 10.
    """
    if description is not None:
        print_before(_("Changing net to {0}").format(netname) )
    
    from preprod.core import concurrent_log
    concurrent_log(f"Before changing net to {netname}")
    
    retry=1
    
    last_string_length=10#len(yellow("[Retrying 1] ."))
    
    while True:
        command=f"nmcli connection up {netname}"
        p=run(command, shell=True,  capture_output=True)
        concurrent_log(command+f" (retry {retry})")
        if p.returncode==10:
            concurrent_log(f"Changing connection throwed {p.returncode} return code ({p.stderr.decode('utf-8')})")
            print_after_error()
            return
            
        for i in range(number_of_sockets):
            try:
                with create_connection((check_host, check_port), timeout=socket_timeout):
                    if description is not None:
                        print_after_ok()
                    concurrent_log(f"After changing net to {netname}")
                    return
            except:
                if retry==1 and i==0:
                    print(" " *last_string_length, end="")
                    stdout.flush()
                    
                s=f"[Retrying {retry}] " +"."*(i+1)
                print("\b"*last_string_length + yellow(s),  end="")
                stdout.flush()
                last_string_length=len(s)
                concurrent_log(f"Connection exception retry {retry}. Socket {i+1}/{number_of_sockets}.")
        retry+=1


def replace_in_file(filename, s, r, number_of_replaces=-1, description=""):
    """
    Replaces all (or up to number_of_replaces) occurrences of a specified string `s` with another string `r`
    within a given file.

    Args:
        filename (str): The path to the file to modify.
        s (str): The string to search for and replace.
        r (str): The replacement string.
        number_of_replaces (int, optional): The maximum number of replacements to perform.
                                            Defaults to -1 (replace all occurrences).
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    description=_("Replacing values in {0}").format(filename) if description=="" else description
    print_before(description, description is not None)
    data=open(filename,"r").read()
    remove(filename)
    data=data.replace(s,r, number_of_replaces)
    with open(filename, "w") as f:
        f.write(data)
    print_after_ok(description is not None)
    from preprod.core import concurrent_log
    concurrent_log(f"Replaced in file '{filename}', '{s}' by '{r}' (max {number_of_replaces} replacements)")

def lines_at_the_end_of_file(filename, s, description=""):
    """
    Appends a given string `s` to the end of a specified file.
    If `s` represents multiple lines, ensure it includes newline characters (`\n`).

    Args:
        filename (str): The path to the file to append to.
        s (str): The string content to append.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    print_before(_("Appending text at the end of {0}").format(filename), description is not None)
    with open(filename, 'a') as f:
        f.write(s)
    print_after_ok(description is not None)
    from preprod.core import concurrent_log
    concurrent_log(f"Added at the of file '{filename}'", s)
    
    

def system(command, user=None, description=""):
    """
    Executes a shell command using `os.system()`.
    Optionally, the command can be run as a different user.

    Args:
        command (str): The shell command string to execute.
        user (str, optional): If provided, the command will be executed as this user
                              using `su - {user} -c "..."`. The current working directory
                              is preserved for the `su` command.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
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
    Executes a shell command using `subprocess.run()` or `subprocess.Popen()`.
    It can optionally run the command as a different user and check its return code
    or standard output against expected values.

    Args:
        command (str): The shell command string to execute.
        user (str, optional): If provided, the command will be executed as this user
                              using `su - {user} -c "..."`.
        userpassword (str, optional): If `user` is provided and the command requires
                                      a password (e.g., for `su`), this password will be
                                      fed to the command's stdin.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
        expected_returncode (int, optional): The expected exit code of the command for it to be considered successful. Defaults to 0.
        expected_stdout (str, optional): A substring expected to be present in the command's standard output for it to be considered successful.
                                         If provided, this check takes precedence over `expected_returncode`.
    Returns:
        bool: True if the command executed successfully according to the checks, False otherwise.
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
    """
    Prints a message to the console indicating the start of an operation.
    The message is prefixed with " - " and does not end with a newline,
    allowing for a subsequent "OK" or "ERROR" status.

    Args:
        s (str): The message to print.
        show (bool, optional): If False, the message will not be printed. Defaults to True.
    """
    if show:
        print (f"  - {s} ",  end="")
        stdout.flush()

def print_after_ok(show=True):
    """
    Prints an "[OK]" status message to the console, typically after `print_before`.

    Args:
        show (bool, optional): If False, the message will not be printed. Defaults to True.
    """
    if show:
        print (f"[{green('OK')}]")

def print_after_error(show=True):
    """
    Prints an "[ERROR]" status message to the console, typically after `print_before`.

    Args:
        show (bool, optional): If False, the message will not be printed. Defaults to True.
    """
    if show:
        print (f"[{red('ERROR')}]")

def rm(filename, description=""):
    """
    Removes a specified file.

    Args:
        filename (str): The path to the file to remove.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    description=_("Removing file '{0}'").format(filename) if description=="" else description
    run_and_check(f"rm '{filename}'", description=description)

def rmtree(directory, show=True):
    """
    Deletes a directory and all its contents recursively.
    If the directory does not exist, no error is raised (`ignore_errors=True`).

    Args:
        directory (str): The path to the directory to remove.
        show (bool, optional): If False, the console output for this operation will be suppressed. Defaults to True.
    """
    print_before(_("Deleting directory {0}").format(directory),show)
    shutil_rmtree(directory, ignore_errors=True)
    print_after_ok(show)
    from preprod.core import concurrent_log
    concurrent_log(f"rmtree('{directory}')")
    
def chdir(directory, show=True):
    """
    Changes the current working directory.

    Args:
        directory (str): The path to the directory to change to.
        show (bool, optional): If False, the console output for this operation will be suppressed. Defaults to True.
    """
    from preprod.core import concurrent_log
    print_before(_("Changing to directory {0}").format(directory),show)
    concurrent_log(f"chdir('{directory}')")
    os_chdir(directory)
    print_after_ok(show)
    
    
def getuser():
    """
    Returns the name of the current logged-in user.

    Returns:
        str: The username of the current user.
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
    Updates the current Git repository by pulling changes from its remote.
    This function executes `git pull`.

    Args:
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    description=_("Pulling git repository") if description=="" else description
    run_and_check("git pull", description=description)

def insert_at_line(file_path, line_number, text, description=""):
    """
    Inserts a new line of text at a specified line number within a file.

    Args:
        file_path (str): The path to the file to modify.
        line_number (int): The 1-based index of the line where the text should be inserted.
                           For example, `line_number=1` inserts at the beginning of the file.
        text (str): The content to insert. A newline character (`\n`) will be appended automatically.
        description (str, optional): A custom description for the console output. If None, no message is printed.
    Raises:
        IndexError: If `line_number` is out of the valid range for the file.
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


def copyfile(from_, to_):
    """
    Copies a file from a source path to a destination path.

    Args:
        from_ (str): The path to the source file.
        to_ (str): The path to the destination file (including the new filename).
    """
    shutil_copyfile(from_,  to_)
    from preprod.core import concurrent_log
    concurrent_log(f"copyfile('{from_}', '{to_}')")

def delete_line_in_file(file_path, line_number, description=""):
    """
    Deletes a specific line from a file.

    Args:
        file_path (str): The path to the file to modify.
        line_number (int): The 1-based index of the line to delete.
        description (str, optional): A custom description for the console output. If None, no message is printed.
    Raises:
        IndexError: If `line_number` is out of the valid range for the file.
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
    Checks if the current user has root privileges.

    Returns:
        bool: True if the current user's UID is 0 (root), False otherwise.
    """
    return getuid() == 0
    
    
def kill_from_ps_aux(pattern, description=""):
    """
    Searches for processes matching a given case-sensitive pattern in `ps aux` output and attempts to kill them.
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
    Determines the base path for the preprod repository.
    It's `/etc/preprod/` for the root user and `~/.preprod/` for normal users.
    Returns:
        str: The absolute path to the preprod repository.
    """
    if is_root():
        return "/etc/preprod/"
    else:
        return f"{path.expanduser('~')}/.preprod/"
        
def check_repository_path(verbose=False):
    """
    Checks if the preprod repository path exists.

    Args:
        verbose (bool, optional): If True, prints an error message and exits
                                  if the repository path does not exist. Defaults to False.
    Returns:
        bool: True if the repository path exists, False otherwise.
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
    Scans the preprod repository and returns a dictionary mapping project names
    to a list of their available action files.

    Returns:
        dict: A dictionary where keys are project names (str) and values are lists of action names (str).
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

def create_python_virtual_env(python_version_name="python3", system_site_packages=False, env_name=None):
    """
    Creates a Python virtual environment.

    Args:
        python_version_name (str, optional): The name of the Python executable to use for creating the virtual environment (e.g., "python3.11"). Defaults to "python3".
        system_site_packages (bool, optional): If True, the virtual environment will have access to the system-wide site-packages. Defaults to False.
        env_name (str, optional): The name of the directory to create the virtual environment in.
                                  If None, it defaults to `.{python_version_name}` (e.g., `.python3`).
                                  This should be a directory name, not a full path. Defaults to None.
    Returns:
        tuple: A tuple containing two absolute paths:
               (path_to_python_executable_in_venv, path_to_pip_executable_in_venv).
    """
    str_sss="--system-site-packages" if system_site_packages else ""
    env_name=f".{python_version_name}" if env_name is None else env_name
    run_and_check(f"{python_version_name} -m venv {str_sss} {env_name}", description= f"Creating virtual env at {env_name}")
    return path.abspath(f"{env_name}/bin/python3"), path.abspath(f"{env_name}/bin/pip")

def apache_initd_restart(description=""):
    """
    Restarts the Apache web server using its `init.d` script.
    This function executes `/etc/init.d/apache2 restart`.

    Args:
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    description=_("Restarting apache server") if description=="" else description
    run_and_check("/etc/init.d/apache2 restart", description=description)
    
def chown_recursive(path,  user="root",  group="root", description=""):    
    """
    Recursively changes the ownership of files and directories within a given path.

    Args:
        target_path (str): The base path for which to change ownership.
        user (str, optional): The username to set as the owner. Defaults to "root".
        group (str, optional): The group name to set as the owner. Defaults to "root".
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    description=_("Changing '{0}' to owner {1}:{2}").format(path, user,  group) if description=="" else description
    run_and_check(f"find {path} -type f -exec chown -R {user}:{group} {{}} +", description=description)

def chmod_recursive(target_path, directory_permissions="755", file_permissions="644", description=""):
    """
    Recursively changes the file permissions for directories and files within a given path.

    Args:
        target_path (str): The base path for which to change permissions.
        directory_permissions (str, optional): The octal permission string for directories (e.g., "755"). Defaults to "755".
        file_permissions (str, optional): The octal permission string for files (e.g., "644"). Defaults to "644".
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    description=_("Changing directories permissions to {0} and files to {1}").format(directory_permissions, file_permissions) if description=="" else description
    run_and_check(f"find {target_path} -type d -exec chmod -R {directory_permissions} {{}} +", description=None)
    run_and_check(f"find {target_path} -type f -exec chmod -R {file_permissions} {{}} +", description=description)


def create_a_file(filename, content="", description=""):
    """
    Creates a new file at the specified `filename` or overwrites an existing one
    with the given `content`.

    Args:
        filename (str): The path and name of the file to create.
        content (str, optional): The string content to write to the file. Defaults to an empty string.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    description=_(f"Creating file '{filename}'") if description=="" else description
    print_before(description, description is not None)
    with open(filename, "w") as f:
        f.write(content)
    print_after_ok(description is not None)
    from preprod.core import concurrent_log
    concurrent_log(description, content)

def npm_install(description=""):
    """
    Executes the `npm install` command to install Node.js dependencies.
    This command should be run in a directory containing a `package.json` file.

    Args:
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    run_and_check("npm install", description=description)
    
def rsync(from_, to_, delete_after=False, description=""):
    """
    Synchronizes files and directories using `rsync`.

    Args:
        from_ (str): The source path(s) for rsync.
        to_ (str): The destination path for rsync.
        delete_after (bool, optional): If True, files that exist on the destination but not on the source
                                       will be deleted after the transfer. Defaults to False.
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    str_delete_after="--delete-after" if delete_after else ""
    run_and_check(f"rsync -avzPH {from_} {to_} {str_delete_after}", description=description)
    
def poetry_install(description=""):
    """
    Executes the `poetry install` command to install project dependencies defined in `pyproject.toml`.

    Args:
        description (str, optional): A custom description for the console output.
                                     If empty, a default message is used. If None, no message is printed.
    """
    run_and_check("poetry install", description=description)
    
def poetry_env_info():
    """
    Retrieves the absolute paths to the Python and Pip executables within the
    Poetry-managed virtual environment for the current project.

    Returns:
        tuple: A tuple containing two strings: (path_to_python_executable, path_to_pip_executable).
    """
    p=run("poetry env info -e", shell=True, capture_output=True)
    python_=p.stdout.decode('utf-8')[:-1]
    pip_=python_.replace("bin/python",  "bin/pip")
    return python_,  pip_

def preprod(project, action, pretend=False, description=""):
    """
        Invokes another preprod action from within the current script.
        Note: This function will terminate the current process if the invoked
        preprod action encounters an error and calls sys.exit().
        
        The `SystemExit` exception is caught to allow for logging and displaying
        an error message, but it is then re-raised to ensure the calling process
        terminates as `preprod.core.main` intends for failed actions.
    Args:
        project (str): The name of the project to invoke.
        action (str): The name of the action within the specified project to invoke.
        pretend (bool, optional): If True, the invoked action will run in pretend mode. Defaults to False.
        description (str, optional): A custom description for the console output. If empty, a default message is used. If None, no message is printed.
    """
    # Lazy import to avoid circular dependency with preprod.core
    from preprod import core
    from preprod.core import concurrent_log

    log_message = _("Invoking preprod action '{0}' for project '{1}'").format(action, project)
    if pretend:
        log_message += _(" (pretend mode)")
    
    description = log_message if description == "" else description
    print_before(description, description is not None)

    args_list = [project, action]
    if pretend:
        args_list.append('--pretend')

    try:
        core.main(args_list)
        # If core.main completes without raising SystemExit, it means the action
        # was considered successful by the core logic.
        print_after_ok(description is not None)
        concurrent_log(log_message + _(" - Succeeded"))
    except SystemExit as e:
        # Catch SystemExit which is raised by core.main when an action
        # explicitly calls sys.exit() due to an error or completion.
        return_code = e.code
        print_after_error(description is not None)
        concurrent_log(log_message + _(" - Failed with exit code {0}").format(return_code))
        raise # Re-raise the SystemExit to ensure the process terminates as core.main intended.
    except Exception as e:
        # Catch any other unexpected exceptions during the action invocation.
        concurrent_log(log_message + _(" - Failed with unexpected error: {0}").format(str(e)))
        raise # Re-raise any other unexpected exception

def sleep(seconds, description=""):
    """
    Pauses the execution for a given number of seconds.

    Args:
        seconds (int or float): The number of seconds to pause.
        description (str, optional): A custom description for the console output. If empty, a default message is used. If None, no message is printed.
    """
    description = _("Sleeping for {0} seconds").format(seconds) if description == "" else description
    print_before(description, description is not None)
    time_sleep(seconds)
    print_after_ok(description is not None)

def create_file(filename, content="", description=""):
    """
    Creates a file with the given filename and content.
    """
    description = _("Creating file '{0}'").format(filename) if description == "" else description
    print_before(description, description is not None)
    with open(filename, "w") as f:
        f.write(content)
    print_after_ok(description is not None)
