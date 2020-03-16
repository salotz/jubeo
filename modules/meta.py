from invoke import task

from ..config import *

@task
def owner(cx):

    print(f"Owner: {owner_name}")
    print(f"Email: {owner_email}")
    print(f"Nickname: {owner_nickname}")

@task
def env(cx):
    print(f"shell profile: {shell_profile}")
    print(f"refugue domain: {refugue_domain}")

@task
def license(cx):
    print(f"License: {project_copyright}")

@task(post=[owner, license, env])
def info(cx):
    print(f"Project: {project_name}")
