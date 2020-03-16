from invoke import task

from ..config import (
    PROJECT_DIR,
)

import joblib

jlmem = joblib.Memory(f"{PROJECT_DIR}/cache/joblib")

@task
def clear(cx):

    jlmem.clear()
