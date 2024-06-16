from argparse import ArgumentParser
from datetime import datetime
from gettext import translation
from importlib.resources import files
from multiprocessing import Lock
from os import path, makedirs
from preprod import commons
from sys import exit
from preprod import __version__, __versiondate__
from getpass import getuser

try:
    t=translation('preprod', files("preprod") / 'locale')
    _=t.gettext
except:
    _=str

def argparse_epilog():
    return _("Developed by Mariano Muñoz 2023-{}").format(__versiondate__.year)

def concurrent_log(title, stdout=None,  stderr=None):
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

## If arguments is None, launches with sys.argc parameters. Entry point is toomanyfiles:main
## You can call with main(['--pretend']). It's equivalento to os.system('program --pretend')
## @param arguments is an array with parser arguments. For example: ['--argument','9'].
def main(arguments=None):
    global lock
    lock=Lock()
    
    global args
    parser=ArgumentParser(description=_("Preprod manager"), epilog= argparse_epilog())
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--pretend', default=False, help=_("Prints action code without running it"),  action='store_true')

    parser.add_argument('project', nargs='?', default=None, help=_("Project identification"),  action='store')
    parser.add_argument('action', nargs='?', default=None, help=_("Action identification"),  action='store')

    args=parser.parse_args(arguments)
    
    commons.check_repository_path(verbose=True)
    repository_path=commons.repository_path()
    project_path=f"{repository_path}/{args.project}/"
    action_path=f"{project_path}/{args.action}"

    
    # Checks for project and action parameters
    if args.project is None and args.action is None:
        list_repository()
        exit(1)
        
    print(commons.yellow(_("Reading repository from '{0}'").format(repository_path)))

    dpa=commons.dictionary_project_actions()
    if not args.project in dpa: 
        print(commons.red(_("Project '{0}' wasn't found en repository. Found projects: {1}").format(args.project, commons.green(str(list(dpa.keys()))))))
        exit(2)
        
    if args.action is None:
        print(commons.red(_("Available actions for project '{0}': {1}").format(args.project,  commons.green(str(dpa[args.project])))))
        exit(3)
        
        
    if not args.action in dpa[args.project]:
        print(commons.red(_("Project '{0}' hasn't '{1}' action. Found actions: {2}").format(args.project,  args.action, commons.green(str(dpa[args.project])))))
        exit(4)
        
    if args.project is not None and args.action is not None:
        start=datetime.now()
        with open(action_path) as f:
            action_commands=f.read()


        commands=f"""
from preprod import commons as preprod_commons
import sys
sys.path.append("{repository_path}")
import repository_commons
{action_commands}
"""
        if args.pretend:
            print(commons.white(_("Pretending project '{0}' and action '{1}':").format(args.project,  args.action)))
            print("________________________________")
            print(commands)
            print("________________________________")
        else:
            print(commons.white(_("Executing project '{0}' and action '{1}'").format(args.project,  args.action)))
            exec(commands)
            print(commons.white(_("Executed project '{0}' and action '{1}' took {2}").format(args.project,  args.action, datetime.now()-start)))


def create():

    parser=ArgumentParser(description=_("Preprod manager"), epilog= argparse_epilog())
    parser.add_argument('--version', action='version', version=__version__)
    parser.parse_args()
    
    if commons.check_repository_path():
        print(_("Repository already created in {}").format(commons.repository_path()))
        exit(6)
    rp=commons.repository_path()
    
    makedirs(f"{rp}/foo/")
    
    with open(f"{rp}/repository_commons.py", "w") as f:
        f.write("""def foo():
    print("This is the ouput of foo_function in repostory commons")
""")
    
    
    with open(f"{rp}/foo/start", "w") as f:
        f.write("""print("This is foo project and start action")
if preprod_commons.is_root():
    print("I'm root")
else:
    print("I'm a normal user")
repository_commons.foo()

""")

def list_repository():
    commons.check_repository_path(verbose=True)
    rp=commons.repository_path()
    print(commons.yellow(_("Reading repository from {0} and listing available preprod scripts").format(rp)))

    dictionary_=commons.dictionary_project_actions()
    ordered_values=list(dictionary_.keys())
    ordered_values.sort()

    for key in ordered_values:
        print(commons.white(key), commons.green(str(dictionary_[key])))
