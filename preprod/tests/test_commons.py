from inspect import currentframe
from preprod import commons, core
from os import system, path

from pytest import raises, fixture

project_test_path=f"{commons.repository_path()}test"
tmp_path="/tmp/preprod_tests"



@fixture(scope='session', autouse=True)
def setup_and_teardown():
    # Code to run at the beginning
    print("Creating preprod test project!")
    system(f"rm -Rf {tmp_path}")
    system(f"mkdir -p {project_test_path}")
    # Anything you need to initialize
    resource = "alltests"

    yield resource  # This allows all tests to run with the resource available

    # Code to run at the end
    system(f"mv {project_test_path}/ {tmp_path}")
    print("Removing preprod test project")
    system(f"rm -Rf {project_test_path}")

    
def create_and_run_action(func_name,  code_):
    """
        Creates a action in repository called test/func_name
        Creates a /tmp/ directory exclusive for this test
        Chdir in this directory
    """
    tmp_test_path=f"{tmp_path}/{func_name}/"
    with open(f"{project_test_path}/{func_name}", "w") as f:
        f.write(f"""
preprod_commons.makedirs("{tmp_test_path}")
preprod_commons.chdir("{tmp_test_path}")
{code_}
""")
    core.main(["test", func_name])
    return tmp_test_path
    
def test_commons_create_python_virtual_env():
    tmp_test_path=create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_python_virtual_env(python_version_name="python3.11", system_site_packages=False)
preprod_commons.create_python_virtual_env(python_version_name="python3.12", system_site_packages=True)
    """)
    assert path.exists(f"{tmp_test_path}/.python3.11/bin/python3.11")
    assert path.exists(f"{tmp_test_path}/.python3.12/bin/python3.12")
    assert commons.file_contains_string(f"{tmp_test_path}/.python3.11/pyvenv.cfg",  "include-system-site-packages = false")
    assert commons.file_contains_string(f"{tmp_test_path}/.python3.12/pyvenv.cfg",  "include-system-site-packages = true")
    
def test_commons_rmtree():
    tmp_test_path=create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.makedirs("to_delete")
preprod_commons.rmtree("to_delete")
    """)
    assert not path.exists(f"{tmp_test_path}/to_delete/")
    
    
def test_commons_git_clone():
    tmp_test_path=create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.git_clone("https://github.com/turulomio/preprod")
preprod_commons.git_clone("https://github.com/turulomio/preprod", "preprod2")
    """)
    assert path.exists(f"{tmp_test_path}/preprod/.git/")
    assert path.exists(f"{tmp_test_path}/preprod2/.git/")
    
def make_test_action():
    print()
    with open(f"{commons.repository_path()}test/test", "w") as f:
        f.write("""
preprod_commons.rmtree("/tmp/preprod_test/")
print("This is foo project and start action")
if preprod_commons.is_root():
    print("I'm root")
else:
    print("I'm a normal user")

preprod_commons.makedirs("/tmp/preprod_test")
preprod_commons.run_and_check("pwd")
preprod_commons.system("pwd")
preprod_commons.chdir("/tmp/preprod_test/")
preprod_commons.git_clone("https://github.com/turulomio/preprod")
preprod_commons.git_clone("https://github.com/turulomio/preprod", "preprod2")
preprod_commons.chdir("/tmp/preprod_test/preprod")
preprod_commons.chown_recursive("/tmp/preprod_test", "dely", "dely")
preprod_commons.chmod_recursive("/tmp/preprod_test")
preprod_commons.npm_install()
preprod_commons.replace_in_file("/tmp/preprod_test/preprod/README.md", "preprod", "preprod_replaced")
preprod_commons.lines_at_the_end_of_file("/tmp/preprod_test/preprod/README.md","THIS IS THE END")
preprod_commons.insert_at_line("/tmp/preprod_test/preprod/README.md", 4, "THIS IS LINE 4")
preprod_commons.delete_line_in_file("/tmp/preprod_test/preprod/README.md", 5)

preprod_commons.git_pull()
preprod_commons.copyfile("README.md", "OTHERREADME.md")

preprod_commons.rsync("README.md", "ANOTHERREADME.md")

preprod_commons.poetry_install()
print(preprod_commons.poetry_env_info())
preprod_commons.apache_initd_restart()

preprod_commons.getuser()

preprod_commons.rm("OTHERREADME.md")
preprod_commons.rm("OTHERREADME.md")

preprod_commons.create_a_file("OTHERREADME.md", "OTHER README")
""")
    
def test_preprod():
    make_test_action()
    core.main(['test', 'test'])
    
def test_list():
    make_test_action()
    with raises(SystemExit):
        core.main([])
    
    with raises(SystemExit):
        core.main(["test2"])
    with raises(SystemExit):
        core.main(["test", "test2"])
        
    core.main(['test', 'test', '--pretend'])

    
def test_list_repository():
    core.list_repository()


    
