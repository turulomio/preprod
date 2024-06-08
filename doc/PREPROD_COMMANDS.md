```text
Help on module preprod.commons in preprod:

NAME
    preprod.commons

FUNCTIONS
    apache_initd_restart(description='')
    
    chdir(directory, show=True)
    
    check_repository_path(verbose=False)
    
    chmod_recursive(path, directory_permissions='755', file_permissions='644', description='')
    
    chown_recursive(path, user='root', group='root', description='')
    
    copyfile(from_, to_)
    
    create_python_virtual_env(python_version_name='python3.11', system_site_packages=False)
        Will create a python virtual env in .python_version_name with python_version_name executable
        Parameters:
           - python_version_name: str: python3.11
    
    delete_line_in_file(file_path, line_number, description='')
    
    dictionary_project_actions()
    
    exit(status=None, /)
        Exit the interpreter by raising SystemExit(status).
        
        If the status is omitted or None, it defaults to zero (i.e., success).
        If the status is an integer, it will be used as the system exit status.
        If it is another kind of object, it will be printed and the system
        exit status will be one (i.e., failure).
    
    getuid()
        Return the current process's user id.
    
    git_clone(url, output_directory='', description='')
    
    git_pull(description='')
    
    green(s)
    
    insert_at_line(file_path, line_number, text, description='')
        Parameters
          - line_number is the number of lines not a zero-based index
          - text must be the content of a line without
    
    is_root()
        Returns if current user is root
    
    lines_at_the_end_of_file(filename, s, description='')
    
    listdir(path=None)
        Return a list containing the names of the files in the directory.
        
        path can be specified as either str, bytes, or a path-like object.  If path is bytes,
          the filenames returned will also be bytes; in all other circumstances
          the filenames returned will be str.
        If path is None, uses the path='.'.
        On some platforms, path may also be specified as an open file descriptor;\
          the file descriptor must refer to a directory.
          If this functionality is unavailable, using it raises NotImplementedError.
        
        The list is in arbitrary order.  It does not include the special
        entries '.' and '..' even if they are present in the directory.
    
    makedirs(dirname, description='')
        Create directories to last child. If it's already created ignores error
    
    nmcli_net_change(netname, check_host, check_port, description='')
        Parameters:
            - netname with Networkmanager: str
            - ip to check: str or name
            - port to check: int
            - description="" Default description. None doesn't print anything
    
    npm_install(description='')
    
    os_chdir = chdir(path)
        Change the current working directory to the specified path.
        
        path may always be specified as a string.
        On some platforms, path may also be specified as an open file descriptor.
          If this functionality is unavailable, using it raises an exception.
    
    os_system = system(command)
        Execute the command in a subshell.
    
    poetry_env_info()
    
    poetry_install(description='')
    
    press_a_key_to_continue()
    
    print_after_error(show=True)
    
    print_after_ok(show=True)
    
    print_before(s, show=True)
    
    red(s)
    
    remove(path, *, dir_fd=None)
        Remove a file (same as unlink()).
        
        If dir_fd is not None, it should be a file descriptor open to a directory,
          and path should be relative; path will then be relative to that directory.
        dir_fd may not be implemented on your platform.
          If it is unavailable, using it will raise a NotImplementedError.
    
    replace_in_file(filename, s, r, description='')
    
    repository_path()
        Returns repository path
    
    rmtree(directory, show=True)
    
    rsync(from_, to_, delete_after=False, description='')
    
    run_and_check(command, description='', expected_returncode=0, expected_stdout=None)
        Executes a comand and returns a boolean if command was executed as expected
    
    system(command, description='')
        Runs a command with system
    
    white(s)
    
    yellow(s)

DATA
    Fore = <colorama.ansi.AnsiFore object>
    Style = <colorama.ansi.AnsiStyle object>
    stdout = <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
    t = <gettext.GNUTranslations object>

FILE
    /home/keko/Proyectos/preprod/preprod/commons.py



```