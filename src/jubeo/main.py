import sys
from pathlib import Path
import pkgutil
import shutil
import os
import os.path as osp
import dataclasses as dc
from typing import (
    Tuple,
)

import toml
from hyperlink import URL
from git import Repo

JUBEO_PROJ_DIR = ".jubeo"

JUBEO_PROJ_CONF = "jubeo.toml"
"""The config file for individual projects."""

TASKSET_NAME = 'tasks'


@dc.dataclass
class ProjConfig():

    upstream_url: URL
    modules_source_url: URL
    modules: Tuple[str]
    taskset_dirname: str

def base_repo_path():

    return Path(sys.modules[__name__].__file__).parent / 'base_repo'

def config_template_path():

    return Path(sys.modules[__name__].__file__).parent / 'config_template'

def get_repo(url, cache_path):

    # if remote download (via git)
    if url.scheme == "git+https":

        # get all but the last '.git' at the end
        repo_name = url.path[-1].replace('.git', '')

        repo_cache_path = Path(cache_path) / repo_name

        print(f"Downloading {repo_name}")
        # remove the "git+" for the cloning
        git_repo = Repo.clone_from(
            url.replace(scheme="https", fragment="").to_text(),
            repo_cache_path)
        print("Done Downloading")

        git_repo_path = Path(git_repo.working_tree_dir)

        # resolve whether the source bundle is at the toplevel or
        # within
        if url.fragment == '':
            source_repo_path = git_repo_path

        else:
            source_repo_path = git_repo_path / url.fragment


    elif url.scheme == "https" or url.scheme == "http":
        raise NotImplementedError("Please use a local file, or the 'git+https' scheme")

    elif url.scheme == '' or url.scheme == 'file':

        print("Retrieving from local repository.")

        # if it is a rooted path add the root
        if url.rooted:
            origin_repo_path = Path('/' + '/'.join(url.path))
        else:
            origin_repo_path = Path('/'.join(url.path))


        # get all but the last '.git' at the end
        repo_name = url.path[-1]

        repo_cache_path = Path(cache_path) / repo_name

        # copy the repo to the cache since we will be manipulating it
        shutil.copytree(
            origin_repo_path,
            repo_cache_path,
        )

        source_repo_path = repo_cache_path / url.fragment

    else:
        raise ValueError(f"URL for upstream jubeo spec invalid: {url.to_text()}")

    return source_repo_path

def retrieve_upstream(
        url: URL,
        cache_path: Path,
        proj_config: ProjConfig,
):

    # TODO: use ProjConfig API, now we are just using a dict

    cach_path = Path(cache_path)
    repo_cache_path = cache_path / "specs"

    # get the spec repo
    upstream_repo_path = get_repo(url, repo_cache_path)

    ## Retrieve external modules

    # we support retrieving modules from a 3rd party source via URL

    mod_source_url = URL.from_text(
        osp.expandvars(osp.expanduser(proj_config['modules']['source_url'])))
    modules = proj_config['modules']['modules']

    # then get the modules repo if any where requested
    if len(modules):

        mod_cache_path = cache_path / "modules"
        mod_repo_path = get_repo(mod_source_url, mod_cache_path)

        # then copy the modules to the source repo
        for module in modules:
            mod_fname = f"{module}.py"
            shutil.copyfile(
                mod_repo_path / mod_fname,
                upstream_repo_path / 'tasks' / 'modules' / mod_fname,
            )

    return upstream_repo_path


def load_proj_config(proj_dir):

    proj_config_path = Path(proj_dir) / JUBEO_PROJ_DIR / JUBEO_PROJ_CONF
    proj_config = toml.load(proj_config_path)

    return proj_config


def update_project(
        source,
        target,
        config,
        force=True
):

    # configuration folder
    source_config = Path(source) / JUBEO_PROJ_DIR
    target_config = Path(target) / JUBEO_PROJ_DIR

    update_config(
        source_config,
        target_config,
        force=force,
    )

    # taskset dir
    source_taskset = Path(source) / TASKSET_NAME
    target_taskset = Path(target) / config['taskset']['dirname']

    update_taskset(
        source_taskset,
        target_taskset,
        config,
        force=force,
    )


def update_config(
        source,
        target,
        force=True,
):
    """Update the configuration files for this project.

    Parameters
    ----------

    source : Path
        The configuration repository to copy from.

    target : Path
        The target configuration folder to update.

    """

    source = Path(source)
    target = Path(target)

    managed_files = (
        'requirements.in',
        'requirements.txt',
    )

    if (any([osp.exists(target / f)
             for f in managed_files])
        and not force):

        raise OSError("Project config exists, not overwriting")

    elif force:
        for f in managed_files:
            f = target / f
            if osp.isdir(f):
                print(f"Cleaning {f}")
                shutil.rmtree(f)
            elif osp.isfile(f):
                print(f"Cleaning {f}")
                os.remove(f)

    print("Updating .jubeo/requirements.in")
    shutil.copyfile(
        source / "requirements.in",
        target / "requirements.in"
    )

    print("Updating .jubeo/requirements.txt")
    shutil.copyfile(
        source / "requirements.txt",
        target / "requirements.txt"
    )


def update_taskset(
        source,
        target,
        config,
        force=True,
):
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

    managed_files = (
        '__init__.py',
        'sysconfig.py',
        'modules',
    )

    if (any([osp.exists(target / f)
             for f in managed_files])
        and not force):

        raise OSError("Project taskset file exists, not overwriting")

    elif force:
        for f in managed_files:
            f = target / f
            if osp.isdir(f):
                print(f"Cleaning {f}")
                shutil.rmtree(f)
            elif osp.isfile(f):
                print(f"Cleaning {f}")
                os.remove(f)

    # then get modules we need and replace the ones in this project
    # with them
    print("Updating tasks/sysconfig.py")
    shutil.copyfile(
        source / "sysconfig.py",
       target / "sysconfig.py"
    )

    print("Updating tasks/__init__.py")
    shutil.copyfile(
        source / "__init__.py",
        target / "__init__.py"
    )

    print("Updating tasks/modules")
    shutil.copytree(
        source / "modules",
        target / "modules",
    )

def init_project(
        source_repo,
        target_project,
        force=False,
):

    source_repo = Path(source_repo)
    target_project = Path(target_project)

    # load the configuration in the source repo
    proj_config = load_proj_config(source_repo)

    ## configuration directory

    configdir_source = source_repo / JUBEO_PROJ_DIR
    configdir_target = target_project / JUBEO_PROJ_DIR

    # make the config directory
    os.makedirs(configdir_target, exist_ok=True)

    # copy the config file: since the update config doesn't manage it
    configfile_source = configdir_source / JUBEO_PROJ_CONF
    configfile_target = configdir_target / JUBEO_PROJ_CONF

    if osp.exists(configfile_target):

        if not force:
            raise OSError("Configuration file exists, not overwriting")

    shutil.copyfile(
        configfile_source,
        configfile_target,
    )

    # not all of the taskset is taken care of by init so do that here
    taskset_source = source_repo / TASKSET_NAME
    taskset_target = target_project / proj_config['taskset']['dirname']

    if osp.exists(taskset_target) and force:
        shutil.rmtree(taskset_target)

    shutil.copytree(
        taskset_source,
        taskset_target,
        dirs_exist_ok=force,
        ignore=shutil.ignore_patterns("*~"),
    )

    # then just use update to copy everything else just to make sure
    update_project(
        source_repo,
        target_project,
        proj_config,
        force=True,
    )
