"""Configuration managed by the system. All changes here will be
overwrote upon update.

Typically gives a collection of good defaults. Override in config.py

"""

### Cleaning

CLEAN_EXPRESSIONS = [
    "\"*~\"",
]


### Envs

# which virtual environment tool to use: venv or conda
ENV_METHOD = 'venv'

# which env spec to use by default
DEFAULT_ENV = 'dev'

# directory where env specs are read from
ENVS_DIR = 'envs'

### Git

INITIAL_VERSION = '0.0.0a0.dev0'
GIT_LFS_TARGETS = []
VERSION = '0.0.0a0.dev0'

### Org-mode

EXE_DIRS = []
TANGLE_DIRS = []

### Project

# the path to the project
PROJECT_DIR = '.'
PROJECT_DIRS = []
RESOURCES = []
RESOURCE_DIR = None

### Python

# the docs for python don't really mean much for analytics projects, a
# different style will be used
BENCHMARK_STORAGE_URL = None
ORG_DOCS_SOURCES = []
RST_DOCS_SOURCES = []

# also not really useful here since we won't be publishing any
# packages on the PyPI indexes
PYPIRC="$HOME/.pypirc"
TESTING_PYPIRC="$HOME/.pypirc"
