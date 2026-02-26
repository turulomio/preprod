```text
Help on module preprod.commons in preprod:

NAME
    preprod.commons

FUNCTIONS
    apache_initd_restart(description='')
        Restarts the Apache web server using its `init.d` script.
        This function executes `/etc/init.d/apache2 restart`.

        Args:
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    chdir(directory, show=True)
        Changes the current working directory.

        Args:
            directory (str): The path to the directory to change to.
            show (bool, optional): If False, the console output for this operation will be suppressed. Defaults to True.

    check_repository_path(verbose=False)
        Checks if the preprod repository path exists.

        Args:
            verbose (bool, optional): If True, prints an error message and exits
                                      if the repository path does not exist. Defaults to False.
        Returns:
            bool: True if the repository path exists, False otherwise.

    chmod_recursive(
        target_path,
        directory_permissions='755',
        file_permissions='644',
        description=''
    )
        Recursively changes the file permissions for directories and files within a given path.

        Args:
            target_path (str): The base path for which to change permissions.
            directory_permissions (str, optional): The octal permission string for directories (e.g., "755"). Defaults to "755".
            file_permissions (str, optional): The octal permission string for files (e.g., "644"). Defaults to "644".
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    chown_recursive(path, user='root', group='root', description='')
        Recursively changes the ownership of files and directories within a given path.

        Args:
            target_path (str): The base path for which to change ownership.
            user (str, optional): The username to set as the owner. Defaults to "root".
            group (str, optional): The group name to set as the owner. Defaults to "root".
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    copyfile(from_, to_)
        Copies a file from a source path to a destination path.

        Args:
            from_ (str): The path to the source file.
            to_ (str): The path to the destination file (including the new filename).

    create_a_file(filename, content='', description='')
        Creates a new file at the specified `filename` or overwrites an existing one
        with the given `content`.

        Args:
            filename (str): The path and name of the file to create.
            content (str, optional): The string content to write to the file. Defaults to an empty string.
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    create_file(filename, content='', description='')
        Creates a file with the given filename and content.

    create_python_virtual_env(
        python_version_name='python3',
        system_site_packages=False,
        env_name=None
    )
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

    delete_line_in_file(file_path, line_number, description='')
        Deletes a specific line from a file.

        Args:
            file_path (str): The path to the file to modify.
            line_number (int): The 1-based index of the line to delete.
            description (str, optional): A custom description for the console output. If None, no message is printed.
        Raises:
            IndexError: If `line_number` is out of the valid range for the file.

    dictionary_project_actions()
        Scans the preprod repository and returns a dictionary mapping project names
        to a list of their available action files.

        Returns:
            dict: A dictionary where keys are project names (str) and values are lists of action names (str).

    epilog()
        Generates the epilog string for the argument parser, including version information.

        Returns:
            str: A formatted string containing the developer's name and the project's version date.

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

    getcwd()
        Return a unicode string representing the current working directory.

    getuid()
        Return the current process's user id.

    getuser()
        Returns the name of the current logged-in user.

        Returns:
            str: The username of the current user.

    git_clone(url, output_directory='', branch=None, description='')
        Clones a git project using its url. If you need a different output directory you can set in params

    git_pull(description='')
        Updates the current Git repository by pulling changes from its remote.
        This function executes `git pull`.

        Args:
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    green(s)
        Returns the input string formatted in bright green color for console output.

        Args:
            s (str): The string to colorize.
        Returns:
            str: The colorized string.

    insert_at_line(file_path, line_number, text, description='')
            Inserts a new line of text at a specified line number within a file.

            Args:
                file_path (str): The path to the file to modify.
                line_number (int): The 1-based index of the line where the text should be inserted.
                                   For example, `line_number=1` inserts at the beginning of the file.
                text (str): The content to insert. A newline character (`
        `) will be appended automatically.
                description (str, optional): A custom description for the console output. If None, no message is printed.
            Raises:
                IndexError: If `line_number` is out of the valid range for the file.

    is_root()
        Checks if the current user has root privileges.

        Returns:
            bool: True if the current user's UID is 0 (root), False otherwise.

    kill_from_ps_aux(pattern, description='')
        Searches for processes matching a given case-sensitive pattern in `ps aux` output and attempts to kill them.

    lines_at_the_end_of_file(filename, s, description='')
            Appends a given string `s` to the end of a specified file.
            If `s` represents multiple lines, ensure it includes newline characters (`
        `).

            Args:
                filename (str): The path to the file to append to.
                s (str): The string content to append.
                description (str, optional): A custom description for the console output.
                                             If empty, a default message is used. If None, no message is printed.

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
        Creates a directory and any necessary parent directories.
        If the directory already exists, no error is raised.

        Args:
            dirname (str): The path of the directory to create.
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    nmcli_net_change(
        netname,
        check_host,
        check_port,
        socket_timeout=2,
        number_of_sockets=5,
        description=''
    )
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

    npm_install(description='')
        Executes the `npm install` command to install Node.js dependencies.
        This command should be run in a directory containing a `package.json` file.

        Args:
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    os_chdir = chdir(path)
        Change the current working directory to the specified path.

        path may always be specified as a string.
        On some platforms, path may also be specified as an open file descriptor.
        If this functionality is unavailable, using it raises an exception.

    os_system = system(command)
        Execute the command in a subshell.

    poetry_env_info()
        Retrieves the absolute paths to the Python and Pip executables within the
        Poetry-managed virtual environment for the current project.

        Returns:
            tuple: A tuple containing two strings: (path_to_python_executable, path_to_pip_executable).

    poetry_install(description='')
        Executes the `poetry install` command to install project dependencies defined in `pyproject.toml`.

        Args:
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    preprod(project, action, pretend=False, description='')
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

    press_a_key_to_continue()
        Pauses script execution and waits for the user to press any key.
        A log entry is made before and after the wait.

    print_after_error(show=True)
        Prints an "[ERROR]" status message to the console, typically after `print_before`.

        Args:
            show (bool, optional): If False, the message will not be printed. Defaults to True.

    print_after_ok(show=True)
        Prints an "[OK]" status message to the console, typically after `print_before`.

        Args:
            show (bool, optional): If False, the message will not be printed. Defaults to True.

    print_before(s, show=True)
        Prints a message to the console indicating the start of an operation.
        The message is prefixed with " - " and does not end with a newline,
        allowing for a subsequent "OK" or "ERROR" status.

        Args:
            s (str): The message to print.
            show (bool, optional): If False, the message will not be printed. Defaults to True.

    red(s)
        Returns the input string formatted in bright red color for console output.

        Args:
            s (str): The string to colorize.
        Returns:
            str: The colorized string.

    remove(path, *, dir_fd=None)
        Remove a file (same as unlink()).

        If dir_fd is not None, it should be a file descriptor open to a directory,
          and path should be relative; path will then be relative to that directory.
        dir_fd may not be implemented on your platform.
          If it is unavailable, using it will raise a NotImplementedError.

    replace_in_file(filename, s, r, description='')
        Replaces all occurrences of a specified string `s` with another string `r`
        within a given file.

        Args:
            filename (str): The path to the file to modify.
            s (str): The string to search for and replace.
            r (str): The replacement string.
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    repository_path()
        Determines the base path for the preprod repository.
        It's `/etc/preprod/` for the root user and `~/.preprod/` for normal users.
        Returns:
            str: The absolute path to the preprod repository.

    rm(filename, description='')
        Removes a specified file.

        Args:
            filename (str): The path to the file to remove.
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    rmtree(directory, show=True)
        Deletes a directory and all its contents recursively.
        If the directory does not exist, no error is raised (`ignore_errors=True`).

        Args:
            directory (str): The path to the directory to remove.
            show (bool, optional): If False, the console output for this operation will be suppressed. Defaults to True.

    rsync(from_, to_, delete_after=False, description='')
        Synchronizes files and directories using `rsync`.

        Args:
            from_ (str): The source path(s) for rsync.
            to_ (str): The destination path for rsync.
            delete_after (bool, optional): If True, files that exist on the destination but not on the source
                                           will be deleted after the transfer. Defaults to False.
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    run_and_check(
        command,
        user=None,
        userpassword=None,
        description='',
        expected_returncode=0,
        expected_stdout=None
    )
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

    sleep(seconds, description='')
        Pauses the execution for a given number of seconds.

        Args:
            seconds (int or float): The number of seconds to pause.
            description (str, optional): A custom description for the console output. If empty, a default message is used. If None, no message is printed.

    system(command, user=None, description='')
        Executes a shell command using `os.system()`.
        Optionally, the command can be run as a different user.

        Args:
            command (str): The shell command string to execute.
            user (str, optional): If provided, the command will be executed as this user
                                  using `su - {user} -c "..."`. The current working directory
                                  is preserved for the `su` command.
            description (str, optional): A custom description for the console output.
                                         If empty, a default message is used. If None, no message is printed.

    time_sleep = sleep(object, /)
        sleep(seconds)

        Delay execution for a given number of seconds.  The argument may be
        a floating-point number for subsecond precision.

    white(s)
        Returns the input string formatted in bright white color for console output.

        Args:
            s (str): The string to colorize.
        Returns:
            str: The colorized string.

    yellow(s)
        Returns the input string formatted in bright yellow color for console output.

        Args:
            s (str): The string to colorize.
        Returns:
            str: The colorized string.

DATA
    Fore = <colorama.ansi.AnsiFore object>
    PIPE = -1
    Style = <colorama.ansi.AnsiStyle object>
    __versiondate__ = datetime.date(2026, 2, 26)
    stdout = <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
    t = <gettext.GNUTranslations object>

VERSION
    1.4.0

FILE
    /home/worky/Proyectos/preprod/preprod/commons.py



```