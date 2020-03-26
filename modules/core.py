from invoke import task

@task
def sanity(cx):
    """Perform sanity check for jubeo"""

    print("All systems go!")


@task
def pin_deps(cx, repo='base'):
    """Pins or upgrades the requirements.txt for the jubeo tooling from
    the requirements.in (from the upstream repo) and the
    local.requirements.in (for project specific tooling dependencies)
    files."""

    repo_path = Path("repos") / repo

    assert osp.exists(repo_path), f"No repo named: {repo}"

    req_in = repo_path / '.jubeo' / "requirements.in"
    local_req_in = repo_path / '.jubeo' / "local.requirements.in"
    req_txt = repo_path / '.jubeo' / "requirements.txt"

    assert osp.exists(req_in), "No 'requirements.in' file"

    # add the local reqs if given
    if osp.exists(local_req_in):
        req_str = f"{req_in} {local_req_in}"
    else:
        req_str = req_in

    cx.run(f"pip-compile --upgrade --output-file={req_txt} {req_str}")
