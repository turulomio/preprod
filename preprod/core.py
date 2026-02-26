from argparse import ArgumentParser
from datetime import datetime
from gettext import translation
from importlib.resources import files
from multiprocessing import Lock
from os import path, makedirs, system
from . import commons, __version__, __versiondate__
from sys import exit
from getpass import getuser
from os import environ # For EDITOR environment variable
from shutil import which # For checking editor availability

try:
    t=translation('preprod', files("preprod") / 'locale')
    _=t.gettext
except:
    _=str


"""
This module provides the core functionality for the preprod command-line tool,
including argument parsing, action execution, and logging.
"""
def concurrent_log(title, stdout=None,  stderr=None):
    """
    Logs messages concurrently to a project-specific log file in /tmp/.
    Includes timestamps, project/action context, and optional stdout/stderr.

    Parameters:
        - title (str): The main log message.
        - stdout (str, optional): Standard output to log.
        - stderr (str, optional): Standard error captured from a command, if any.
    """
    def parse_std(std):
        arr=std.split("\n")
        r=""
        for line in arr:
            r+=f"      {line}\n"
        return r
    filename=f"/tmp/preprod_logs_{getuser()}/{args.project}.log"
    makedirs(path.dirname(filename), exist_ok=True)
    with lock:
        with open(filename, "a") as f:
            f.write(commons.yellow(f"{datetime.now()} [{args.project}/{args.action}] {title}\n"))
            if stdout!="" and stdout is not None:
                f.write(commons.green("      STDOUT\n"))
                f.write(parse_std(stdout))
            if stderr!="" and stderr is not None:
                f.write(commons.red("      STDERR\n"))
                f.write(parse_std(stderr))

def main(arguments=None):
    """
    The main entry point for the preprod application.

    Parses command-line arguments, validates project and action, and executes
    the specified action script. It also handles 'pretend' and 'edit' modes.

    Parameters:
        arguments (list, optional): A list of strings representing command-line
                                    arguments. If None, `sys.argv` is used.
                                    Example: `['--pretend', 'myproject', 'myaction']`.
                                    This allows programmatic invocation similar to `os.system('program --pretend')`.
    """
    global lock
    # `lock` is a multiprocessing.Lock used for ensuring exclusive access
    # to the log file during concurrent logging operations. It's initialized
    # globally here because `concurrent_log` is called from various places
    # and needs a shared lock instance.
    lock=Lock()
    
    global args
    parser=ArgumentParser(description=_("Preprod manager"), epilog= commons.epilog()) # Corrected epilog call
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--pretend', default=False, help=_("Prints action code without running it"),  action='store_true')
    parser.add_argument('--edit', default=False, help=_("Opens the action file in the default console editor"), action='store_true')

    parser.add_argument('project', nargs='?', default=None, help=_("Project identification"),  action='store')
    parser.add_argument('action', nargs='?', default=None, help=_("Action identification"),  action='store')

    # `args` is a global variable storing the parsed command-line arguments.
    # It's made global to be accessible by functions like `concurrent_log`
    # which need access to `args.project` and `args.action` for context.
    # This avoids passing `args` explicitly to every function.
    args=parser.parse_args(arguments)
    
    commons.check_repository_path(verbose=True)
    repository_path=commons.repository_path()
    project_path=f"{repository_path}/{args.project}/"
    action_path=f"{project_path}/{args.action}"

    
    # Checks for project and action parameters
    if args.project is None and args.action is None:
        # If no project or action is specified, list all available projects
        # and their actions, then exit. This serves as a default behavior
        # for simply running `preprod`.
        list_repository()
        exit(1)
        
    print(commons.yellow(_("Reading repository from '{0}'").format(repository_path)))

    dpa=commons.dictionary_project_actions()
    if not args.project in dpa: 
        # If the specified project is not found, inform the user and exit.
        print(commons.red(_("Project '{0}' wasn't found en repository. Found projects: {1}").format(args.project, commons.green(str(list(dpa.keys()))))))
        exit(2)
        
    if args.action is None:
        # If a project is specified but no action, list available actions
        # for that project and exit.
        print(commons.red(_("Available actions for project '{0}': {1}").format(args.project,  commons.green(str(dpa[args.project])))))
        exit(3)
        
        
    if not args.action in dpa[args.project]:
        # If the specified action is not found within the project, inform
        # the user and exit.
        print(commons.red(_("Project '{0}' hasn't '{1}' action. Found actions: {2}").format(args.project,  args.action, commons.green(str(dpa[args.project])))))
        exit(4)
        
    if args.edit:
        editor_command = environ.get('EDITOR')
        if not editor_command:
            if which('mcedit'):
                editor_command = 'mcedit'
            elif which('nano'):
                editor_command = 'nano'
            else:
                editor_command = 'vi' # Fallback to vi if no other editor found or EDITOR env var not set

        # Open the action file in the determined editor.
        system(f"{editor_command} {action_path}")
        exit(0) # Exit after editing

    if args.project is not None and args.action is not None:
        start=datetime.now()
        # Read the action commands from the specified action file.
        # These commands are expected to be Python code.
        # The `with open(...)` ensures the file is properly closed.
        # The `action_path` is constructed from the repository, project, and action names.
        with open(action_path) as f:
            action_commands=f.read()


        commands=f"""
from preprod import commons as preprod_commons
import sys
sys.path.append("{repository_path}")
import repository_commons
""" + action_commands + """
"""
        if args.pretend:
            # In pretend mode, print the commands that would be executed
            # without actually running them.
            print(commons.white(_("Pretending project '{0}' and action '{1}':").format(args.project,  args.action)))
            print("________________________________")
            print(commands)
            print("________________________________")
        else:
            # Execute the combined Python commands. This includes importing
            # `preprod_commons` and `repository_commons` for use within the action script.
            print(commons.white(_("Executing project '{0}' and action '{1}'").format(args.project,  args.action)))
            exec(commands)
            print(commons.white(_("Executed project '{0}' and action '{1}' took {2}").format(args.project,  args.action, datetime.now()-start)))


def create():
    """
    Initializes a new preprod repository.
    This function sets up the basic directory structure for preprod,
    creates a sample project ('foo') with a 'start' action, and
    generates a `repository_commons.py` file with a sample function.
    Creates the necessary directory structure and a sample project/action
    along with a `repository_commons.py` file.
    """
    parser=ArgumentParser(description=_("Preprod manager"), epilog= commons.epilog()) # Corrected epilog call
    parser.add_argument('--version', action='version', version=__version__)
    parser.parse_args()
    
    if commons.check_repository_path():
        print(_("Repository already created in {}").format(commons.repository_path()))
        exit(6)
    # Determine the repository path based on user privileges (root or normal user).
    rp=commons.repository_path()
    
    makedirs(f"{rp}/foo/")
    
    # Create a sample `repository_commons.py` file.
    with open(f"{rp}/repository_commons.py", "w") as f:
        f.write("""def foo():
    print("This is the ouput of foo_function in repostory commons")
""")
    
    
    with open(f"{rp}/foo/start", "w") as f:
        # Create a sample action file 'start' within the 'foo' project.
        f.write("""print("This is foo project and start action")
if preprod_commons.is_root():
    print("I'm root")
else:
    print("I'm a normal user")
repository_commons.foo()

""")

def list_repository():
    """
    Lists all available preprod projects and their actions in the repository.

    It first checks if the repository path exists, then retrieves a dictionary
    mapping project names to a list of their actions. The output is sorted
    alphabetically by project name and displayed in a user-friendly format
    with color coding.
    Prints a formatted output of the discovered projects and actions.
    """
    commons.check_repository_path(verbose=True)
    rp=commons.repository_path()
    print(commons.yellow(_("Reading repository from {0} and listing available preprod scripts").format(rp)))

    dictionary_=commons.dictionary_project_actions()
    ordered_values=list(dictionary_.keys())
    ordered_values.sort()

    for key in ordered_values:
        print(commons.white(key), commons.green(str(dictionary_[key])))
