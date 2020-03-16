from invoke import task

from .config import config

CLEAN_EXPRESSIONS = [
    "\"*~\"",
]


@task
def ls_clean(cx):

    for clean_expr in CLEAN_EXPRESSIONS:
        cx.run('find . -type f -name {} -print'.format(clean_expr))

@task(ls_clean)
def clean(cx):
    print("Deleting Targets")
    for clean_expr in CLEAN_EXPRESSIONS:
        cx.run('find . -type f -name {} -delete'.format(clean_expr))

