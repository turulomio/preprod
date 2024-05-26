#!/usr/bin/python3
from argparse import ArgumentParser
from datetime import datetime
from gettext import translation
from importlib.resources import files
from multiprocessing import Lock
from os import path, makedirs
from preprod import commons
from sys import exit


try:
    t=translation('preprod', files("preprod") / 'locale')
    _=t.gettext
except:
    _=str


def concurrent_log(title, stdout=None,  stderr=None):
    def parse_std(std):
        arr=std.split("\n")
        r=""
        for line in arr:
            r+=f"      {line}\n"
        return r
    filename=f"/tmp/preprod_logs/{args.project}.log"
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
            
def main():
    global lock
    lock=Lock()

    parser=ArgumentParser(description=_("ProPred manager"))
    parser.add_argument('--pretend', default=False, help=_("Prints action code without running it"),  action='store_true')

    parser.add_argument('project',nargs='?', default=None, help=_("Project identification"),  action='store')
    parser.add_argument('action',nargs='?', default=None, help=_("Action identification"),  action='store')

    global args
    args=parser.parse_args()
    
    commons.check_repository_path(verbose=True)
    repository_path=commons.repository_path()
    project_path=f"{repository_path}/{args.project}/"
    action_path=f"{project_path}/{args.action}"
    
    if args.project is None and args.action is None:
        list()
        exit(10)
    

    print(commons.yellow(_("Reading repository from {0}").format(repository_path)))
    if not (args.project and path.exists(project_path)):
        print(commons.red(_("Project wasn't found in {0}").format(project_path)))
        exit(5)
    if not (args.action and path.exists(action_path)):
        print(commons.red(_("Action wasn't found in {0}").format(action_path)))
        exit(5)
        
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
            print("________________________________")
            print(commands)
            print("________________________________")
        else:
            print(commons.white(_("Executing project '{0}' and action '{1}'").format(args.project,  args.action)))
            exec(commands)
            print(commons.white(_("Executed project '{0}' and action '{1}' took {2}").format(args.project,  args.action, datetime.now()-start)))


def create():

    parser=ArgumentParser(description=_("ProPre manager"))
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

def list():

    parser=ArgumentParser(description=_("ProPre manager"))    
    parser.add_argument('--repository_commons', default=False, help=_("Shows repository_commons.py file in repository pathh"),  action='store_true')

    args=parser.parse_args()
    
    commons.check_repository_path(verbose=True)
    rp=commons.repository_path()
    print(commons.yellow(_("Reading repository from {0} and listing available preprod scripts").format(rp)))

    if args.repository_commons:
        with open(f"{rp}/repository_commons.py", "r") as f:
            print(f.read())
            exit(0)
        

    for key, value in commons.dictionary_project_actions().items():
        print(commons.white(key), commons.green(str(value)))
