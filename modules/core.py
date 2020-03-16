from invoke import task

from ..config import *


@task()
def test(cx):

    # TODO: tests to run on the consistency and integrity of the repo

    # prefix all of these tests by activating the dev environment
    with cx.prefix(" {{cookiecutter.project_slug}}.dev"):
        cx.run("conda activate {{cookiecutter.project_slug}}.dev && inv -l",
               pty=True)
