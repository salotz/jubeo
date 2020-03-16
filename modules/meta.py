from invoke import task

from ..config import (
    OWNER_NAME,
    OWNER_EMAIL,
    OWNER_NICKNAME,
    PROJECT_COPYRIGHT,
    PROJECT_NAME,
)

@task
def owner(cx):

    print(f"Owner: {OWNER_NAME}")
    print(f"Email: {OWNER_EMAIL}")
    print(f"Nickname: {OWNER_NICKNAME}")

@task
def license(cx):
    print(f"License: {PROJECT_COPYRIGHT}")

@task(post=[owner, license])
def info(cx):
    print(f"Project: {PROJECT_NAME}")
