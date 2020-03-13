import shutil
import os.path as osp

import click

from .main import (
    tasks_template_path,
)

@click.command()
@click.option("--force")
@click.option("--output", default="tasks")
@click.argument('project-dir', type=click.Path(exists=True))
def init(force, output, project_dir):

    template_dir_path = tasks_template_path()

    target = Path(project_dir) / output

    shutil.copytree(
        template_dir_path,
        target,
        dirs_exist_ok=force,
    )


@click.command()
@click.argument('task-path', type=click.Path(exists=True))
def update(task_path):

    # first read the task dir config file to get the URL to download things from

    # then download (via git)
    _ = Repo.clone_from(update_url,
                           repo_path)

    # TODO
    cx.run(f"cp -f {repo_path}/" +
           "*cookiecutter.project_name*/tasks/sysconfig.py ./tasks/sysconfig.py",
           pty=True)

    cx.run(f"cp -f {repo_path}/" +
           "*cookiecutter.project_name*/tasks/__init__.py ./tasks/__init__.py",
           pty=True)

    cx.run(f"cp -rf {repo_path}/" +
           "*cookiecutter.project_name*/tasks/modules/ ./tasks/")


@click.group()
def cli():
    pass

cli.add_command(update)
cli.add_command(init)

if __name__ == "__main__":

    cli()
