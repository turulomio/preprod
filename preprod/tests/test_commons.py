from preprod import commons, core
from os import system

    
def make_test_action():
    print()
    system(f"mkdir -p {commons.repository_path()}test")
    with open(f"{commons.repository_path()}test/test", "w") as f:
        f.write("""
print("This is foo project and start action")
if preprod_commons.is_root():
    print("I'm root")
else:
    print("I'm a normal user")
repository_commons.foo()

preprod_commons.makedirs("/tmp/probe")
preprod_commons.run_and_check("pwd")
preprod_commons.system("pwd")
preprod_commons.chown_recursive("/tmp/probe", "dely", "dely")
preprod_commons.chdir("/tmp/probe")
preprod_commons.npm_install()
preprod_commons.git_clone("https://github.com/turulomio/preprod")
preprod_commons.git_clone("https://github.com/turulomio/preprod", "preprod2")(
        """)
    
def test_preprod():
    make_test_action()
    core.main(['foo', 'start'])
    
