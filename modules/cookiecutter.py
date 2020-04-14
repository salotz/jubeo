import json
from pathlib import Path

from invoke import task

from ..config import (
    COOKIECUTTER_TEST_DIR,
)

def render_from_json(
        template_url,
        settings_json,
        target_path,
):
    from cookiecutter.main import cookiecutter

    settings = json.loads(settings_json)

    cookiecutter(
        str(template_url),
        extra_context=settings,
        output_dir=target_path,
        no_input=True,
        overwrite_if_exists=True,
    )


@task
def clean(cx):

    cx.run(f"rm -rf tests/{COOKIECUTTER_TEST_DIR}")

@task(pre=[clean])
def test_render(cx, context=None):

    from cookiecutter.main import cookiecutter

    # make sure the test dir exists
    cx.run(f"mkdir -p tests/{COOKIECUTTER_TEST_DIR}")

    template_url = Path(".")

    if context is None:

        context_json = json.dumps({})
        output_dir = Path('tests') / COOKIECUTTER_TEST_DIR

    else:

        # the path to the context JSON file
        context_path = Path(f"tests/test_contexts/{context}.json")
        context_json = context_path.read_text()
        output_dir = Path('tests') / COOKIECUTTER_TEST_DIR

    render_from_json(
        template_url,
        context_json,
        output_dir,
        )

@task(pre=[test_render])
def test_rendered_repo(cx, default=True, context=None):
    pass

    # with cx.cd(target_dir):

    #     cx.run()
