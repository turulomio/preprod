from preprod import commons, core
from os import system
from pytest import raises
    
def make_test_action():
    print()
    system(f"mkdir -p {commons.repository_path()}test")
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

preprod_commons.create_python_virtual_env()
preprod_commons.rsync("README.md", "ANOTHERREADME.md")

preprod_commons.poetry_install()
print(preprod_commons.poetry_env_info())
preprod_commons.apache_initd_restart()

preprod_commons.getuser()

preprod_commons.rm("OTHERREADME.md")
preprod_commons.rm("OTHERREADME.md")

preprod_commons.create_a_file("OTHERREADME.md", "OTHER README")
""")
        
def remove_test_project():
    system(f"rm -Rf {commons.repository_path()}test")
    
def test_preprod():
    remove_test_project()
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
