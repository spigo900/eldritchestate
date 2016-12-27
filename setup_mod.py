#!/usr/bin/env python3
from setuptools import find_packages
from cx_Freeze import setup, Executable


SOURCE_DIR = 'src/py'

build_exe_options = {
    "include_files": ['data', 'fonts'],
    "includes": ['cffi', 'tdl', 'ecs', 'six'],  # has to be "six=1.5.2"
    "packages": ['eldestrl'],
}

setup(
    name='eldritch_estate',
    version='0.1.0.dev0',
    package_dir={'': SOURCE_DIR},
    packages=find_packages(SOURCE_DIR),
    install_requires=['tdl',
                      'ecs'],
    classifiers=[
        'Developent Status :: 3 - Alpha'
    ],
    keywords='game roguelike',
    entry_points={'console_scripts': [
        'eldestrl = eldestrl.__main__:main'
    ]},
    options={'build_exe': build_exe_options},
    executables=[Executable(SOURCE_DIR + '/eldestrl/executable.py',
                            targetName='eldestrl.exe')]
)
