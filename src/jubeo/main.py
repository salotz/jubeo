import sys
from pathlib import Path
import pkgutil
import shutil

import toml
import hyperlink
from git import Repo

JUBEO_PROJ_CONF = "jubeo.toml"
"""The config file for individual projects."""


TASKSET_NAME = 'tasks'

def base_repo_path():

    return Path(sys.modules[__name__].__file__).parent / 'base_repo'

def config_template_path():

    return Path(sys.modules[__name__].__file__).parent / 'config_template'

def retrieve_upstream(url, cache_path):

    # if remote download (via git)
    if url.scheme == "git+https":

        print("Downloading...")
        # remove the "git+" for the cloning
        git_repo_path = Repo.clone_from(
            url.replace(scheme="https").to_text(),
            cache_path)
        print("Done Downloading")

        # resolve whether the source bundle is at the toplevel or
        # within
        if url.fragment == '':
            source_repo_path = git_repo_path

        else:
            source_repo_path = Path(url.fragment)


    elif url.scheme == "https" or url.scheme == "http":
        raise NotImplementedError("Please use a local file, or the 'git+https' scheme")

    elif url.scheme == '' or url.scheme == 'file':
        source_repo_path = '/' + '/'.join(url.path)

    else:
        raise ValueError(f"URL for upstream jubeo spec invalid: {url.to_text()}")


    return source_repo_path



def load_proj_config(proj_jubeo_dir):

    proj_config_path = Path(proj_jubeo_dir) / JUBEO_PROJ_CONF
    proj_config = toml.load(proj_config_path)

    return proj_config


def update_project(source, target, config):

    source_taskset = Path(source) / 'tasks'
    target_taskset = Path(target) / config['taskset']['dirname']

    update_taskset(source_taskset, target_taskset)

def update_taskset(source, target):
    """Update the taskset for this project.

    Parameters
    ----------

    source : Path
        The task-set repository to copy from.

    target : Path
        The target task-set to update.

    """

    source = Path(source)
    target = Path(target)

    # read the configuration file
    

    # then get modules we need and replace the ones in this project
    # with them
    print("Updating tasks/sysconfig.py")
    shutil.copyfile(
        source / "sysconfig.py",
        target / "sysconfig.py"
    )
    # cx.run(f"cp -f {repo_path}/" +
    #        "*cookiecutter.project_name*/tasks/sysconfig.py ./tasks/sysconfig.py",
    #        pty=True)

    print("Updating tasks/__init__.py")
    # cx.run(f"cp -f {repo_path}/" +
    #        "*cookiecutter.project_name*/tasks/__init__.py ./tasks/__init__.py",
    #        pty=True)

    print("Updating tasks/modules")
    # cx.run(f"cp -rf {repo_path}/" +
    #        "*cookiecutter.project_name*/tasks/modules/ ./tasks/")


