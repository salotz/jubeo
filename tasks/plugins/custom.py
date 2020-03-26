"""Put user defined tasks in the plugins folder. You can start with
some customizations in this file which is included by default."""

from invoke import task

import os.path as osp
from pathlib import Path


@task
def pin_repo_deps(cx, repo='base'):
    """Pins or upgrades pins of the specified repo's dependency specs."""

    repo_path = Path("repos") / repo

    assert osp.exists(repo_path), f"No repo named: {repo}"

    req_in = repo_path / '.jubeo' / "requirements.in"
    req_txt = repo_path / '.jubeo' / "requirements.txt"

    assert osp.exists(req_in), "No 'requirements.in' file"

    cx.run(f"pip-compile --upgrade --output-file={req_txt} {req_in}")

