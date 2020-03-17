
# SNIPPET: add this to import modules

from . import hello

# should be copied in by the installation process
from . import core
from . import clean
from . import env
from . import git
from . import py

MODULES = [
    hello,
    core,
    clean,
    env,
    git,
    py,
]
