#!/usr/bin/env python
# setup.py
#
# (C) 2020, Daniel Mouritzen

from setuptools import setup

requirements = [
    'appdirs',
    'attrs',
    'loguru',
    'pysimplegui',
]

test_requirements = [
    'mypy',
    'pyflakes',
    'pytest',
    'pytest-flake8',
    'pytest-isort',
    'pytest-mypy',
]

setup(
    name='TaskManager',
    version='0.0.0',
    description='',
    author='Daniel Mouritzen',
    author_email='dmrtzn@gmail.com',
    url='https://github.com/Danmou/TaskManager',
    packages=['task_manager'],
    python_requires='>=3.7',
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=test_requirements,
    extras_require={'test': test_requirements},
    entry_points={'console_scripts': ['TaskManager=task_manager.gui:main']},
)
