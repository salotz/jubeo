import shutil
import os
import os.path as osp
from pathlib import Path

import click

from hyperlink import URL
import toml

from .main import (
    base_repo_path,
    config_template_path,
    retrieve_upstream,
    load_proj_config,
    update_project,
)

CONFIG_DIR = "$XDG_CONFIG_HOME/.jubeo"
"""The system-wide configuration directory, including configuring the
jubeo tool itself"""

JUBEO_CONF_NAME = "jubeo_conf.toml"
"""Configures the behavior of the jubeo tool."""

def load_config():

    config_path = Path(osp.expandvars(CONFIG_DIR)) / JUBEO_CONF_NAME
    config = toml.load(config_path)

    return config

def init_cache():

    config = load_config()
    os.makedirs(config['cache']['path'],
                exist_ok=True)

@click.command()
@click.option("--force/--no-force", default=False)
def init_config(force):
    """Initialize the system-wide configuration directory."""

    config_dir_path = config_template_path()

    conf_dir = Path(osp.expandvars(CONFIG_DIR))

    if osp.exists(conf_dir) and force:
        shutil.rmtree(conf_dir)

    shutil.copytree(
        config_dir_path,
        conf_dir,
        dirs_exist_ok=force,
        # ignore the mod def which is needed for pkgutils
        ignore=shutil.ignore_patterns("*~", "__init__.py"),
    )


@click.command()
def clean_cache():
    """Remove cached files."""

    config = load_config()

    shutile.rmtree(config['cache']['path'])

    init_cache()


# TODO: unify jubeo-base repo with the one in here
@click.command()
@click.option("--force/--no-force", default=False)
@click.option("--taskset-name", default="tasks")
@click.option('--upstream', type=str, default=None)
@click.argument('project-dir', type=click.Path(exists=True))
def init(force, taskset_name, upstream, project_dir):
    """Initialize a project task-set."""

    project_dir = Path(project_dir)

    config = load_config()

    cache_path = Path(config['cache']['path'])

    # get the upstream repo we are retrieving from, downloading if
    # necessary
    if upstream is None:
        upstream_url = URL.from_text(str(base_repo_path()))
    else:
        upstream_url = URL.from_text(upstream)

    source_repo_path = Path(retrieve_upstream(upstream_url, cache_path))

    init_repo(source, target, config)
    ## taskset
    taskset_target = project_dir / taskset_name
    taskset_source = source_repo_path / TASKSET_NAME

    if osp.exists(taskset_target) and force:
        shutil.rmtree(taskset_target)

    shutil.copytree(
        taskset_source,
        taskset_target,
        dirs_exist_ok=force,
        ignore=shutil.ignore_patterns("*~"),
    )


    ## config file installation
    proj_config_source = Path(source_repo_path) / JUBEO_PROJ_CONF
    proj_conf_target = project_dir / JUBEO_PROJ_CONF

    if osp.exists(proj_conf_target):

        if not force:
            raise OSError("Configuration file exists, not overwriting")

    shutil.copyfile(
        proj_config_source,
        proj_conf_target
    )


@click.command()
@click.argument('project-dir', type=click.Path(exists=True))
def update(project_dir):
    """Update a projects task-set."""

    project_dir = Path(project_dir)

    # read the system-wide configuration file to find location of the
    # cache directory
    config = load_config()

    # load the project config
    proj_config = load_proj_config(project_dir)

    # TODO: do I need that stem
    cache_path = Path(config['cache']['path']) # / project_dir.stem

    # get the upstream URL
    url_str = osp.expandvars(proj_config['upstream_url'])
    url = URL.from_text(url_str)

    # retrieve the upstream repo and return the exact file location of
    # the jubeo bundle
    source_repo_path = retrieve_upstream(url, cache_path)

    ## update the project
    update_project(source_repo_path,
                   project_dir,
                   proj_config)


@click.group()
def cli():
    pass

cli.add_command(update)
cli.add_command(init)
cli.add_command(clean_cache)
cli.add_command(init_config)

if __name__ == "__main__":

    cli()
