from invoke import task
import os


@task
def reformat(c):
    c.run("black music_metadata_filter tests setup.py tasks.py")


@task
def lint(c):
    c.run("flake8 music_metadata_filter tests tasks.py")
    c.run("black --check --diff music_metadata_filter tests setup.py")


@task
def test(c):
    args = ["pytest", "--cov=music_metadata_filter", "--cov-branch", "--cov-report=term"]
    if os.environ.get("CI", "false") != "true":
        args.append("--cov-report=html")

    c.run(" ".join(args))


@task
def type_check(c):
    c.run("mypy music_metadata_filter tests")
