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
    
def test_commons_git_pull():
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.git_clone("https://github.com/turulomio/preprod")
preprod_commons.chdir("preprod")
preprod_commons.git_pull()
    """)    
    
def test_commons_run_and_check():
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.run_and_check("pwd")
    """)    
    

def test_commons_chown_recursive():
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("hello", "")
preprod_commons.chown_recursive("hello")
    """)
    
def test_commons_chmod_recursive():
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("hello", "")
preprod_commons.chmod_recursive("hello")
    """)
    

def test_commons_replace_in_file():   
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("hello.txt", "hello")
preprod_commons.replace_in_file("hello.txt", "hello", "bye")
    """)
    assert commons.file_contains_string("hello.txt",  "bye")
    
def test_commons_lines_at_the_end_of_file():   
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("numbers.txt", "one\\n")
preprod_commons.lines_at_the_end_of_file("numbers.txt", "two")
    """)
    assert commons.file_contains_string("numbers.txt",  "two")
    
def test_commons_insert_at_line():   
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("numbers.txt", "one\\nthree")
preprod_commons.insert_at_line("numbers.txt", 2, "two")
    """)
    
    with open("numbers.txt",  "r") as f:
        line=f.readlines()
        assert "two" in line[1]

def test_commons_delete_line_in_file():   
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("numbers.txt", "one\\ntwo\\nthree")
preprod_commons.delete_line_in_file("numbers.txt", 2,)
    """)
    assert not commons.file_contains_string("numbers.txt",  "two")
    
def test_commons_copyfile():   
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("hello.txt", "")
preprod_commons.copyfile("hello.txt", "bye.txt")
    """)
    assert path.exists("hello.txt")
    assert path.exists("bye.txt")     
    
def test_commons_rm():   
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("hello.txt","")
preprod_commons.rm("hello.txt")
    """)
    assert not path.exists("hello.txt")
    
    
def test_commons_rsync():   
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.create_a_file("hello.txt", "")
preprod_commons.rsync("hello.txt", "bye.txt")
    """)
    assert path.exists("hello.txt")
    assert path.exists("bye.txt")
        

def test_commons_poetry_install():
    create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.git_clone("https://github.com/turulomio/django_calories_tracker")
preprod_commons.chdir("django_calories_tracker")
preprod_commons.poetry_install()
    """)
    
    assert "preprod-hsKAf-PM" in commons.poetry_env_info()[0]

def test_commons_npm_install():
    tmp_test_path=create_and_run_action(currentframe().f_code.co_name,  """
preprod_commons.git_clone("https://github.com/turulomio/calories_tracker")
preprod_commons.chdir("calories_tracker")
preprod_commons.npm_install()
    """)
    assert path.exists(f"{tmp_test_path}/calories_tracker/node_modules/")

    
def test_list():
    with raises(SystemExit):
        core.main([])
    
    with raises(SystemExit):
        core.main(["test2"])
    with raises(SystemExit):
        core.main(["test", "test2"])
        
    core.main(['test', 'test_commons_run_and_check', '--pretend'])

    
def test_list_repository():
    core.list_repository()


    
