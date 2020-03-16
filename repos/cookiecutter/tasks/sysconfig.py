"""Configuration managed by the system. Do not make changes you aren't
afraid of being overwritten and removed automatically."""

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

