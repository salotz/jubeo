from invoke import task

@task(default=True)
def hello(cx):
    """Example task from an installed module"""

    print("Hello from the jubeo author.")
