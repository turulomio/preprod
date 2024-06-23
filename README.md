# PreProd [![PyPI - Downloads](https://img.shields.io/pypi/dm/preprod?label=Pypi%20downloads)](https://pypi.org/project/preprod/) [![Tests](https://github.com/turulomio/preprod/actions/workflows/python-app.yml/badge.svg)](https://github.com/turulomio/preprod/actions/workflows/python-app.yml)
Easy creation of pre-production and production scripts to automate your deployment

When you're deploying your software in your web server or when you're developing, you often need to modify default settings of your software to addapt them to your needs.

Sometimes, you develop your own scripts to automate this task, but these scripts become more complex each day. That's the reason of this project. PreProd helps you to develop your own deployment script, setting them in a repository.

Preprod uses python code so you don't have to learn any other language.

If your user is root this repository is set in `/etc/preprod` and if your logged as a normal user in `~/.preprod`

Preprod has defined a lot of help commands to make your scripts more visual. They are resumed below and you can call them appending `preprod_commons` python module. Morever you can create your own commands in `{yourrepositorypath}/repository_commons.py` and call them inside your scripts appending `repository_commons` as any other python module.

## Example

For example, We are going to automate e2e test in console using preprod with my frontend project [Calories Tracker](https://github.com/turulomio/calories_tracker/)

First we need to create our PreProd repository. As we said before you can create as root or as a normal user.


```bash
preprod_create_repository
cd /home/your_user/.preprod
mkdir calories_tracker
nano calories_tracker/build
```

In calories_tracker/build add the next code

```python
preprod_commons.chdir("/tmp")
preprod_commons.rmtree("/tmp/calories_tracker_build")
preprod_commons.git_clone("https://github.com/turulomio/calories_tracker", "calories_tracker_build")
preprod_commons.chdir("/tmp/calories_tracker_build")
preprod_commons.npm_install()
preprod_commons.run_and_check("npm run build")
```

Now if you run `preprod` you can see your scripts (project: calories_tracker, action: build). So just run

```bash
preprod calories_tracker build
```
You'll see in console 

<img src="https://raw.githubusercontent.com/turulomio/preprod/main/doc/preprod_example.png" title="PreProd example">

And your calories_tracker build is now in `/tmp/calories_tracker_build/dist` 

If something goes wrong you can see color logs in `/tmp/preprod_logs_your_user/`

I hope you like it and give me a star.

## Commands

You can see all preprod_commons method  [here](doc/PREPROD_COMMANDS.md)


## Changelog

### 0.6.0 (2024-06-23)
- Solved problem creating python virtual environment
- Improving tests procedure. Coverage is now 85% (#42)

### 0.5.0 (2024-06-17)
- Added getuser, rm, create_a_file commands
- Improved preprod parameters experience
- poetry_env_info now returns a tuple with the virtual env python executable and pip executable

### 0.4.0 (2024-06-08)
- Temporal preprod logs are now created by each user to avoid permissions problems
- Added examples and documentation
- Added poe doc command
- Improved parameters errors

### 0.3.0 (2024-05-28)
- Improved description system
- Added makedirs and git clone in different directory
- Improved spanish translations
- Added --version to commands
- Added test with a 84% coverture

### 0.2.0 (2024-05-26)
- Added logs in /tmp/preprod_logs/
- Added chown_recursive, chmod_recursive, rsync, poetry_install, poetry_env_info methods to commons

### 0.1.0 (2024-05-21)
- Basic functionality
