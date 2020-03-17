from invoke import task

#@task(pre=[clean])
@task
def test_render(cx, default=True, context_file=None):

    cx.run("mkdir -p tests/_test_builds")

    if default:
        cx.run("cookiecutter -f --no-input -o tests/_test_builds/ .")

    # read from a JSON file
    elif context_file is not None:
        assert osp.exists(context_file), f"context file {context_file} doesn't exist"

        cx.run(f"cookiecutter -f --no-input -o tests/_test_builds/ . {context}")

    # otherwise do interactively
    else:
        cx.run("cookiecutter -f -o tests/_test_builds/ .")


@task(pre=[test_render])
def test_rendered_repo(cx, default=True, context=None):

    default_name = "default_repo_name"
    target_dir = f'tests/_test_builds/{default_name}'

    with cx.cd(target_dir):

        print("testing the generated repo is okay")
        print(f"cd {target_dir}")
        cx.run("inv repo-test", echo=True)


