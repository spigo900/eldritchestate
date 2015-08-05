#!/usr/bin/env python3
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
import sys
from shutil import sh

SOURCE_DIR = 'src/py'


class install(_install):
    def run(self):
        sh('untdl.patch')
        _install.run(self)


class develop(_develop):
    def run(self):
        sh('untdl.patch')
        _develop.run(self)


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
    install_requires=['untdl',
                      'ecs'],
    tests_require=['pytest', 'flake8', 'pytest-flake8'],
    cmdclass={'test': PyTest,
              'install': install,
              'develop': develop},
    classifiers=[
        'Developent Status :: 3 - Alpha'
    ],
    entry_points={'console_scripts': [
        'eldestrl = eldestrl.main:main'
    ]}
)
