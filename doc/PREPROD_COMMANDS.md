```text
Help on module preprod.commons in preprod:

NAME
    preprod.commons

FUNCTIONS
    apache_initd_restart(description='')
        Starts apache using init.d script

    chdir(directory, show=True)
        Changes to a directory

    check_repository_path(verbose=False)
        Gets with a boolean if repository path exists

    chmod_recursive(path, directory_permissions='755', file_permissions='644', description='')

    chown_recursive(path, user='root', group='root', description='')

    copyfile(from_, to_)
        Copies a file

    create_a_file(filename, content, description='')
        Creates a new file or replaces it with content parameter

    create_python_virtual_env(python_version_name='python3.11', system_site_packages=False)
        Will create a python virtual env in .python_version_name with python_version_name executable
        Parameters:
           - python_version_name: str: python3.11

    delete_line_in_file(file_path, line_number, description='')
        Deletes a line in a file

    dictionary_project_actions()
        Returns a dictioanry with all projects and actions

    exit(status=None, /)
        Exit the interpreter by raising SystemExit(status).

        If the status is omitted or None, it defaults to zero (i.e., success).
        If the status is an integer, it will be used as the system exit status.
        If it is another kind of object, it will be printed and the system
        exit status will be one (i.e., failure).

    file_contains_string(file_path, search_string)
        Check if the specified file contains the given string.

        Args:
        file_path (str): The path to the file.
        search_string (str): The string to search for in the file.

        Returns:
        bool: True if the file contains the string, False otherwise.

    getuid()
        Return the current process's user id.

    getuser()
        Returns a string with current user

    git_clone(url, output_directory='', description='')
        Clones a git project using its url. If you need a different output directory you can set in params

    git_pull(description='')
        Updates git repository using git pull command

    green(s)
        Prints string in green and bright color

    insert_at_line(file_path, line_number, text, description='')
        Inserts a line using the number of the line

        Parameters
          - line_number is the number of lines not a zero-based index
          - text must be the content of a line without

    is_root()
        Returns if current user is root

    lines_at_the_end_of_file(filename, s, description='')
                Appends a string (for lines append
        ) to the end of the file

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
        Uses nmcli to change a net and waits until can connect to check_host:check_port

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
        Return the path to the python executable and pip executable inside current dir poetry virtualenv

    poetry_install(description='')

    press_a_key_to_continue()
        Waits until user press a key

    print_after_error(show=True)

    print_after_ok(show=True)

    print_before(s, show=True)

    red(s)
        Prints string in red and bright color

    remove(path, *, dir_fd=None)
        Remove a file (same as unlink()).

        If dir_fd is not None, it should be a file descriptor open to a directory,
          and path should be relative; path will then be relative to that directory.
        dir_fd may not be implemented on your platform.
          If it is unavailable, using it will raise a NotImplementedError.

    replace_in_file(filename, s, r, description='')
        Replaces a string for other in the whole file

    repository_path()
        Returns repository path

    rm(filename, description='')
        Removes a file

    rmtree(directory, show=True)
        Deletes a directory recursively. It directory doesn't exist ignores error

        Be careful

    rsync(from_, to_, delete_after=False, description='')

    run_and_check(command, description='', expected_returncode=0, expected_stdout=None)
        Executes a comand and returns a boolean if command was executed as expected

    system(command, description='')
        Runs a command with system

    white(s)
        Prints string in white and bright color

    yellow(s)
        Prints string in yellow and bright color

DATA
    Fore = <colorama.ansi.AnsiFore object>
    Style = <colorama.ansi.AnsiStyle object>
    result = False
    stdout = <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
    t = <gettext.GNUTranslations object>

FILE
    /home/keko/Proyectos/preprod/preprod/commons.py



```