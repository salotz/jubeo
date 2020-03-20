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
    init_project,
    load_proj_config,
    update_project,
)

CONFIG_DIR = "$XDG_CONFIG_HOME/jubeo"
"""The system-wide configuration directory, including configuring the
jubeo tool itself"""

JUBEO_CONF_NAME = "jubeo_conf.toml"
"""Configures the behavior of the jubeo tool."""

def load_config():

    config_path = Path(osp.expandvars(CONFIG_DIR)) / JUBEO_CONF_NAME
    config = toml.load(config_path)

    return config

def _init_cache():

    config = load_config()
    cache_path = Path(osp.expandvars(osp.expanduser(config['cache']['path'])))

    os.makedirs(cache_path,
                exist_ok=True)

    # make the sub directories needed
    os.makedirs(cache_path / 'specs',
                exist_ok=True)
    os.makedirs(cache_path / 'modules',
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

    _init_cache()



def _clean_cache():
    """Remove cached files."""

    config = load_config()

    try:
        shutil.rmtree(osp.expanduser(osp.expandvars(config['cache']['path'])))
    except FileNotFoundError:
        _init_cache()
    else:
        _init_cache()



@click.command()
def clean_cache():
    _clean_cache()


@click.command()
@click.option("--force/--no-force", default=False)
@click.option("--taskset-name", default="tasks")
@click.option('--upstream', type=str, default=None)
@click.argument('project-dir', type=click.Path(exists=True))
def init(force, taskset_name, upstream, project_dir):
    """Initialize a project task-set."""

    _clean_cache()

    project_dir = Path(project_dir)

    config = load_config()

    cache_path = Path(osp.expanduser(osp.expandvars(config['cache']['path'])))

    # get the upstream repo we are retrieving from, downloading if
    # necessary
    if upstream is None:
        upstream_url = URL.from_text(str(base_repo_path()))
    else:
        upstream_url = URL.from_text(upstream)

    # then we can simply copy from this downloaded repo
    source_repo_path = Path(retrieve_upstream(upstream_url, cache_path))

    init_project(
        source_repo_path,
        project_dir,
        force=force,
    )



@click.command()
@click.argument('project-dir', type=click.Path(exists=True))
def update(project_dir):
    """Update a projects task-set."""

    # we don't do a fancy caching strategy and redownload every time
    # now, so we clean everytime now
    _clean_cache()

    project_dir = Path(project_dir)

    # read the system-wide configuration file to find location of the
    # cache directory
    config = load_config()

    # load the project config
    proj_config = load_proj_config(project_dir)

    cache_path = Path(osp.expanduser(osp.expandvars(config['cache']['path'])))

    # get the upstream URL
    url_str = osp.expandvars(proj_config['upstream_url'])
    url = URL.from_text(url_str)

    module_url = URL.from_text(
        osp.expandvars(osp.expanduser(proj_config['modules']['source_url'])))

    print(f"Using upstream: {url}")
    print(f"Retrieving modules from: {module_url}")

    # retrieve the upstream repo and return the exact file location of
    # the jubeo bundle
    source_repo_path = retrieve_upstream(
        url,
        cache_path,
        proj_config,
    )

    ## update the project
    update_project(
        source_repo_path,
        project_dir,
        proj_config,
        force=True,
    )


@click.group()
def cli():
    pass

cli.add_command(update)
cli.add_command(init)
cli.add_command(clean_cache)
cli.add_command(init_config)

if __name__ == "__main__":

    cli()
