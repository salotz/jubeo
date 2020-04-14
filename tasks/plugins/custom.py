"""Put user defined tasks in the plugins folder. You can start with
some customizations in this file which is included by default."""

from invoke import task

import os
import os.path as osp
from pathlib import Path


@task
def pin_repo_deps(cx, repo=None):
    """Pins or upgrades pins of the specified repo's dependency specs.

    If no repo is specified it updates all of them.

    """

    if repo is not None:

        repo_paths = [Path("repos") / repo]

    else:

        repo_paths = [Path("repos") / repo
                      for repo in
                      os.listdir("repos")]

    for repo_path in repo_paths:
        assert osp.exists(repo_path), f"No repo named: {repo}"

        req_in = repo_path / '.jubeo' / "requirements.in"
        req_txt = repo_path / '.jubeo' / "requirements.txt"

        assert osp.exists(req_in), "No 'requirements.in' file"

        cx.run(f"pip-compile --upgrade --output-file={req_txt} {req_in}")

