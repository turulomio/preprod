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
    Runs the pytest test suite with code coverage analysis.
    It generates a coverage report in the console and an HTML report
    for detailed inspection, omitting `repository_commons.py` from coverage.
    """
    system("coverage run --omit='*repository_commons.py' -m pytest && coverage report && coverage html")


def translate():
    """
    Manages the translation process for the project.
    This involves several steps:
    1. Extracts translatable strings from Python source files into a `preprod.pot` template.
    2. Merges new strings into existing Spanish (`es.po`) and English (`en.po`) PO files.
    3. Compiles the updated PO files into machine-object (`.mo`) files, which are used by `gettext` at runtime.
    """
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o preprod/locale/preprod.pot preprod/*.py")
    # `xgettext`: Extracts translatable strings from Python files.
    #   `-L Python`: Specifies Python language.
    #   `--no-wrap`: Prevents wrapping of long lines.
    #   `--no-location`: Does not include source code location.
    #   `--from-code='UTF-8'`: Specifies input encoding.
    #   `-o preprod/locale/preprod.pot`: Output to the Portable Object Template file.
    #   `preprod/*.py`: Specifies source files to scan.
    system("msgmerge -N --no-wrap -U preprod/locale/es.po preprod/locale/preprod.pot")
    system("msgfmt -cv -o preprod/locale/es/LC_MESSAGES/preprod.mo preprod/locale/es.po")
    
def pytest():
    """
    Runs the pytest test suite for the project.
    This command executes all tests discovered by pytest in the project directory.
    """
    system("pytest")

def doc():
    """
    Generates documentation for the `preprod.commons` module and saves it to a Markdown file.
    This function dynamically captures the output of Python's built-in `help()`
    function for `preprod.commons`.
    It temporarily redirects `sys.stdout` to an in-memory buffer (`io.StringIO`)
    to capture the help text, then restores `sys.stdout` and writes the captured
    content to `doc/PREPROD_COMMANDS.md` within a Markdown code block.
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