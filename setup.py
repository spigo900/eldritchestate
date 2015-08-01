from setuptools import setup, find_packages

SOURCE_DIR='src/py'

setup(
    name='eldritch_estate',
    version='0.1.0.dev0',
    package_dir={'': SOURCE_DIR},
    packages=find_packages(SOURCE_DIR),
    install_requires=['untdl'],
    tests_require=['pytest'],
    classifiers=[
        'Developent Status :: 3 - Alpha'
    ]
)
