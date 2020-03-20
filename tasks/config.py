"""User settings for a project."""

# load the system configuration. You can override them in this module,
# but beware it might break stuff
from .sysconfig import *

PROJECT_SLUG = "jubeo"
VERSION="0.0.2a0.dev0"

PYPIRC="$HOME/.pypirc"
TESTING_PYPIRC="$HOME/.salotz.d/lib/configs/pypi/salotz_test.pypirc.ini"
