
# SNIPPET: add this to import modules

from . import hello

# should be copied in by the installation process
from . import core

MODULES = [
    hello,
    core,
]
