from invoke import task


@task
def reformat(c):
    c.run("black music_metadata_filter tests setup.py tasks.py")


@task
def lint(c):
    c.run("flake8 music_metadata_filter tests tasks.py")
    c.run("black --check --diff music_metadata_filter tests setup.py")


@task
def test(c):
    c.run("pytest")


@task
def type_check(c):
    c.run("mypy music_metadata_filter tests")
