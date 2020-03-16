from invoke import task

from ..config import *


@task
def init(cx):
    """Initialize the folder structure and other such fixtures."""


    # create the folder structure
    for d in PROJECT_DIRS:
        cx.run("mkdir -p {}".format(d))
        cx.run("touch {}/.keep".format(d))

@task
def link_resources(ctx):
    """Make links to the project resource folders in this project"""

    for resource in RESOURCES:

        command = "ln -s -r -f -T {res}/{resource} {proj}/{resource}".format(
            res=RESOURCE_DIR,
            proj=PROJECT_DIR,
            resource=resource)

        print("Running")
        print(command)
        print("-----------------------------")
        ctx.run(command)

