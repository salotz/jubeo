from invoke import task

from ..config import *

VCS_RELEASE_TAG_TEMPLATE = "v{}"

@task
def lfs_track(cx):
    """Update all the files that need tracking via git-lfs."""

    for lfs_target in GIT_LFS_TARGETS:
        cx.run("git lfs track {}".format(lfs_target))


@task
def vcs_init(cx):

    initial_version = "{{cookiecutter.initial_version}}"
    tag_string = VCS_RELEASE_TAG_TEMPLATE.format(initial_version)

    cx.run("git init && "
           "git add -A && "
           "git commit -m 'initial commit' && "
           f"git tag -a {tag_string} -m 'initialization release'")
