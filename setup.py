#!/usr/bin/env python

from __future__ import print_function

import getpass
import os
import time

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

long_description_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'README.md')

with open(long_description_filename) as fd:
    long_description = fd.read()

FILENAME = '0wned'
ROOT_PATH = os.path.join(os.path.abspath(os.sep), FILENAME)
USER_PATH = os.path.join(os.path.expanduser('~'), FILENAME)
USER = getpass.getuser()
TIME = int(time.time())


def touch_file():
    try:
        with open(ROOT_PATH, 'a') as root_fd:
            message = 'Created {!r} with user {!r} at {!r}'.format(
                ROOT_PATH,
                USER,
                TIME
            )
            print(message)
            root_fd.write(message + '\n')
    except (IOError, OSError):
        try:
            with open(USER_PATH, 'a') as user_fd:
                message = 'Created {!r} with user {!r} at {!r}'.format(
                    USER_PATH,
                    USER,
                    TIME
                )
                print(message)
                user_fd.write(message + '\n')
        except (IOError, OSError):
            print('Could not write to {!r} or {!r}'.format(ROOT_PATH, USER_PATH))
            print('What kind of tricky system are you running this on?')


class PostDevelopCommand(develop):
    def run(self):
        touch_file()
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        touch_file()
        install.run(self)


setup(
    name='0wned',
    version='0.6.0',
    description='Code execution via Python package installation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mschwager/0wned',
    packages=[],
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
    ],
    install_requires=[],
    tests_require=[],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
