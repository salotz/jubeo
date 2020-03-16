from invoke import task

from ..config import *

import joblib

jlmem = joblib.Memory(f"{PROJECT_DIR}/cache/joblib")

@task
def clear(cx):

    jlmem.clear()
