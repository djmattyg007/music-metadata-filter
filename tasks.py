import os
import shlex
import sys

from invoke import task, util


in_ci = os.environ.get("CI", "false") == "true"
if in_ci:
    pty = False
else:
    pty = util.isatty(sys.stdout) and util.isatty(sys.stderr)


@task
def reformat(c):
    c.run("isort music_metadata_filter tests setup.py tasks.py", pty=pty)
    c.run("black music_metadata_filter tests setup.py tasks.py", pty=pty)


@task
def lint(c):
    c.run("flake8 --show-source --statistics music_metadata_filter tests", pty=pty)


@task
def test(c, onefile=""):
    pytest_args = ["pytest", "--cov=music_metadata_filter", "--cov-branch", "--cov-report=term"]
    if in_ci:
        pytest_args.extend(("--cov-report=xml", "--strict-markers"))
    else:
        pytest_args.append("--cov-report=html")

    if onefile:
        pytest_args.append(shlex.quote(onefile))

    c.run(" ".join(pytest_args), pty=pty)


@task
def type_check(c):
    c.run("mypy music_metadata_filter tests", pty=pty)
