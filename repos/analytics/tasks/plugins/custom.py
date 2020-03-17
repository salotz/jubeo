"""Put user defined tasks in the plugins folder. You can start with
some customizations in this file which is included by default."""

from invoke import task

from ..config import (
    TEST_MESSAGE,
    SYS_TEST_MESSAGE,
)

@task
def hello(cx):
    """An example custom user task from the plugins."""
    print("Hello!")
    print(f"Message from config.py: {TEST_MESSAGE}")
    print(f"Message from sysconfig.py: {SYS_TEST_MESSAGE}")
