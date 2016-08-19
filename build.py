import pytest
from pybuilder.core import use_plugin, init, task, depends

use_plugin("python.install_dependencies")

name = "studentit-bookit-client"
default_task = "install_dependencies"


@task
@depends("unit_tests", "integration_tests")
def all_tests(logger):
    pass


@task
def unit_tests(logger):
    failed = pytest.main(["tests"])

    if failed:
        raise Exception("Unit tests failed")


@task
def integration_tests(logger):
    pass


@task
@depends("install_dependencies", "all_tests")
def build(logger):
    pass


@task
@depends("build")
def publish(logger):
    pass


@init
def set_properties(project):
    project.depends_on_requirements("runtime-requirements.txt")
    project.build_depends_on_requirements("build-requirements.txt")

