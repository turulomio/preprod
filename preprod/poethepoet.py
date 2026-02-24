from preprod import __version__
from os import system

def release():
    """
    Provides instructions for creating a new release of the preprod project.
    """
    print("""Nueva versión:
  * Cambiar la version en pyproject.toml
  * Cambiar la versión y la fecha en __init__.py
  * Editar README.md to add CHANGELOG
  * Ejecutar otra vez poe release
  * git checkout -b preprod-{0}
  * poe doc
  * poe translate
  * nano preprod/locale/es.po
  * poe translate
  * poe coverage
  * git commit -a -m 'preprod-{0}'
  * git push --set-upstream origin preprod-{0}
  * Hacer un pull request con los cambios a main
  * Hacer un nuevo tag en GitHub
  * git checkout main
  * git pull
  * poetry build
  * poetry publish
  * Crea un nuevo ebuild de preprod en Gentoo con la nueva versión
  * Subelo al repositorio myportage

""".format(__version__))

    
def coverage():
    """
    Runs pytest with coverage and generates a coverage report and HTML output.
    """
    system("coverage run --omit='*repository_commons.py' -m pytest && coverage report && coverage html")


def translate():
    """
    Manages translation files for the project.
    Extracts translatable strings, updates PO files, and compiles MO files.
    """
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o preprod/locale/preprod.pot preprod/*.py")
    system("msgmerge -N --no-wrap -U preprod/locale/es.po preprod/locale/preprod.pot")
    system("msgfmt -cv -o preprod/locale/es/LC_MESSAGES/preprod.mo preprod/locale/es.po")
    system("msgfmt -cv -o preprod/locale/en/LC_MESSAGES/preprod.mo preprod/locale/en.po")
    
def pytest():
    """
    Runs the pytest test suite for the project.
    """
    system("pytest")

def doc():
    """
    Generates documentation for preprod.commons module in Markdown format.
    Captures the output of `help(preprod.commons)` and saves it to `doc/PREPROD_COMMANDS.md`.
    """
    import io
    import sys
    import preprod.commons
    # Replace 'module_name' with the actual module name you want to get help for

    # Create a string buffer to capture the help output
    buffer = io.StringIO()

    # Redirect stdout to the buffer
    sys.stdout = buffer

    # Call the help function on the module
    help(preprod.commons)

    # Reset stdout to default
    sys.stdout = sys.__stdout__

    # Get the help output from the buffer
    help_output = buffer.getvalue()

    # Write the help output to a Markdown file
    with open('doc/PREPROD_COMMANDS.md', 'w') as f:
        f.write(f'```text\n{help_output}\n```')

    print("Help output saved to doc/PREPROD_COMMANDS.md")