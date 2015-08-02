from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages
import sys

SOURCE_DIR = 'src/py'


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["tests", "--flake8"]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='eldritch_estate',
    version='0.1.0.dev0',
    package_dir={'': SOURCE_DIR},
    packages=find_packages(SOURCE_DIR),
    install_requires=['untdl'],
    tests_require=['pytest', 'flake8', 'pytest-flake8'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Developent Status :: 3 - Alpha'
    ],
    entry_points={'game': [
        'eldestrl = eldestrl.main:game_loop'
    ]}
)
