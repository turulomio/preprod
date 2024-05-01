#!/usr/bin/python3
from argparse import ArgumentParser
from os import path
from preprod import commons
from sys import exit

_=str


def main():

    parser=ArgumentParser(description=_("ProPre manager"))
    parser.add_argument('project',nargs='?', default=None, help=_("Project identification"),  action='store')
    parser.add_argument('action',nargs='?', default=None, help=_("Project identification"),  action='store')


    args=parser.parse_args()
    
    commons.check_repository_path(verbose=True)
    repository_path=commons.repository_path()
    commons_path=f"{repository_path}/commons"
    project_path=f"{repository_path}/{args.project}/"
    action_path=f"{project_path}/{args.action}"

    print(_("Reading repository from {0}").format(repository_path))
    if not (args.project and path.exists(project_path)):
        print(_("Project wasn't found in {0}").format(project_path))
        exit(5)
    if not (args.action and path.exists(action_path)):
        print(_("Action wasn't found in {0}").format(action_path))
        exit(5)
        
    if args.project is not None and args.action is not None:
        
        with open(action_path) as f:
            action_commands=f.read()


        repository_commons_commands=""
        print(commons_path,  path.exists(commons_path))

        if path.exists(commons_path):
            with open(commons_path) as f:
                repository_commons_commands=f.read()



        commands=f"""
from preprod import commons
{repository_commons_commands}

{action_commands}
        """
        print("________________________________")
        print(commands)
        print("________________________________")

        print(_("Executing project '{0}' and action '{1}'").format(args.project,  args.action))
        exec(commands)
        exit(0)

def create():

    parser=ArgumentParser(description=_("ProPre manager"))
    parser.parse_args()
    
    if commons.check_repository_path():
        print(_("Repository already created in {}").format(commons.repository_path()))
        
    print ("TODO")

def list():

    parser=ArgumentParser(description=_("ProPre manager"))
    parser.parse_args()
    
    commons.check_repository_path(verbose=True)

    for key, value in commons.dictionary_project_actions().items():
        print(key, value)
